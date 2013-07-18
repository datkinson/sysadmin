#!/usr/bin/python
# requires installation of beautifulsoup to run
__author__ = 'datkinson'
import httplib2
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer

http = httplib2.Http()
URL = 'http://hourd.net'
status, response = http.request(URL)
LINKS = {}

# find all links on page
for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
	# if the found link starts with the supplied url then add it to dict
	if link['href'].startswith(URL):
		if link['href'] in LINKS:
			LINKS[link['href']] = LINKS[link['href']]+1
		else:
			LINKS[link['href']] = 1
# loop through the dict adding new links from the new links

# --- need to add ---
LIST_SIZE = 0

# print the dict
for key, value in LINKS.items():
	        print "%s - %d" % (key, value)
