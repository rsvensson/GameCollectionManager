#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

url = "file:///home/synt4x/Nextcloud/Code/Projects/GameCollectionManager/FCWiki.html"

rawHTML = urlopen(url)
html = bs(rawHTML, "html.parser")

# Gets the info from the <tr> tags and saves it to a list

titles = html.find_all("a").get_text()
print(titles)
gamelist = []
startRead = 0
stopRead = 0

"""
for i in range(len(trlist)):

    # Get initial start
    if startRead == 0:
        for j, game in enumerate(trlist):
            if "Title\n" in game:
                startRead = j+1
                break

    for game in trlist[startRead:]:
        if "Title\n" in game:
            startRead = i+1
            print(startRead)
            break
        if game == "" or game == "\n":
            pass

        #temp = game.lstrip().split("\n")
        gamelist.append(game)
"""



#print(trList[10])
#print(type(trList[10]))

#with open("gamelist.txt", 'w', encoding='utf8') as f:
#    f.writelines(trList)