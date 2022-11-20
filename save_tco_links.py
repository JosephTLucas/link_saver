import re
import itertools
import requests
import os
import argparse
import json
from joblib import Parallel, delayed


def remove_emojis(data):
    """
    https://stackoverflow.com/a/58356570
    """
    emoj = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        re.UNICODE,
    )
    return re.sub(emoj, "", data)


def get_likes_with_tco(path):
    with open(f"{path}/data/like.js", "r") as f:
        data = f.read().splitlines()

    data = [remove_emojis(x) for x in data]

    return list(filter(lambda x: len(x) > 0, [filter_for_url(x) for x in data]))


def tokenize(line):
    """ 
    Examples of unsupported parses:
    - ending in punctuation
    - applications.\xa0\xa0https://t.co
    """
    line = line.split("\\n")
    return list(
        itertools.chain.from_iterable([re.split(r',| |"|\(|\)|\\', x) for x in line])
    )


def filter_for_url(line):
    return list(filter(lambda x: "https://t.co" in x, tokenize(line)))


def write_file(path, expanded_urls):
    with open(path, "a") as f:
        f.write("\n".join(expanded_urls))


def expand_url(tco_url):
    for turl in tco_url:
        try:
            url = requests.get(turl, timeout=1.0).url
            print(f"{turl} -> {url}")
            return url
        except Exception as e:
            print(f"Could not fetch {turl}")
            return f"Could not fetch {turl}"


def main(in_dir, out, n):
    tco_links = get_likes_with_tco(in_dir)
    chunk_size = 100
    with Parallel(n_jobs=n, prefer="threads") as parallel:
        for i in range(0, len(tco_links), chunk_size):
            x = i
            expanded = parallel(
                delayed(expand_url)(tco_url)
                for tco_url in tco_links[x : x + chunk_size]
            )
            write_file(out, expanded)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Twitter Like link saver",
        description="Expands links from a twitter archive",
    )
    parser.add_argument("-i", "--in_dir")
    parser.add_argument("-o", "--outfile")
    parser.add_argument("-n", type=int, default=1)
    args = parser.parse_args()
    main(args.in_dir, args.outfile, args.n)
