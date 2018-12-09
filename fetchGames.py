#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

def simpleGet(url):

    # Gets an html file and returns the raw content
    try:
        with closing(get(url, stream=True)) as resp:
            if isGoodResponce(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print("Error during request to {0} : {1}".format(url, str(e)))
        return None

def isGoodResponce(resp):

    # Only returns if content is html
    contentType = resp.headers["Content-Type"].lower()
    return (resp.status_code == 200
            and contentType is not None
            and contentType.find("html") > -1)

# Testing with Wikipedia's list of SNES games page
rawHTML = simpleGet("https://en.wikipedia.org/wiki/List_of_Super_Nintendo_Entertainment_System_games")
html = bs(rawHTML, "html.parser")

# Prints the info from all the <td> tags
for i, td in enumerate(html.select("td")):
    print(i, td.text)
