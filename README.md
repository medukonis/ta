# ta
Python 3 text analysis tool (english language).
Usage: ta.py logfile.log
Output are three files - links.html, hashtags.html, and word listing.txt sorted from word that appeared the most to least.
Keep stop_words.txt and ta_functions.py in same directory
Can analyze any text file however processing function lops off first three or for tokenized words because of my use case which was IRC.
I had no use for the time stamp, nick, and a couple of other items that make up the preamble of each irc sentence but you can adjust
as needed.

Work in progress - added vader sentiment analyzer just before uploading.
