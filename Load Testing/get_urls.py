#!/usr/bin/python
# requires installation of beautifulsoup to run
__author__ = 'datkinson'
import httplib2
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer

http = httplib2.Http()
URL = 'http://hourd.co.uk'
status, response = http.request(URL)
LINKS = {}

def pageLinks(page_url):
	# find all links on page
	global LINKS
	for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
		# if the found link starts with the supplied url then add it to dict
		if link['href'].startswith(URL):
			if link['href'] in LINKS:
				LINKS[link['href']] = LINKS[link['href']]+1
			else:
				LINKS[link['href']] = 1

def printLinks(LIST):
        # print the dict
        for key, value in LIST.items():
                print "%s - %d" % (key, value)

# loop through the dict adding new links from the new links
pageLinks(URL)
LIST_LENGTH = len(LINKS)
TEMP_LIST_LENGTH = 0
while LIST_LENGTH != TEMP_LIST_LENGTH:
	for key, value in LINKS.items():
		pageLinks(key)
	TEMP_LIST_LENGTH = len(LINKS)

printLinks(LINKS)

