# Twitter Link Saver

Create a newline separated text file of expanded links for all of the tweets you've liked (from your twitter archive zip).

For years, I have "liked" tweets on Twitter for their valuable content. This weekend, I exported my data to save some of that content for future reference. However, Twitter shortens links with their [t.co link shortener](https://help.twitter.com/en/using-twitter/url-shortener) and even the `expandedURL` field of the `.js` files is a `twitter.com` link. I wrote this script to ensure that I have the original source links in case the twitter `t.co` redirection is taken offline.

The script currently only looks at the `likes.js` file, but should easy enough to modify for any other needs. I originally wrote it look at all of the files recursively, but Twitter did us the great service of also exporting plenty of advertisement links.\*

## Requirements

- [`joblib`](https://joblib.readthedocs.io/en/latest/parallel.html) to thread the network requests. We're going to be here for awhile. Python is slow, but your network is slower.

- An unzipped [Twitter archive](https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive)

## Usage

`python save_tco_links.py -i <your twitter archive directory (unzipped)> -o <outfile> -n <number of threads>`

Inside the script, there is also a `chunk_size` to configure how often you're writing results to your outfile.


\* Sarcasm aside, I do understand why this might be useful from auditability and research perspectives... I just didn't want to expand them for this use-case.
