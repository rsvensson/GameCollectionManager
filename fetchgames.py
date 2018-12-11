#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

url = "file:///home/synt4x/Nextcloud/Code/Projects/GameCollectionManager/data/html/FDS.html"

rawHTML = urlopen(url)
html = bs(rawHTML, "html.parser")

titleColumn = 0
#wtitleColumn = 0

tr = html.find_all("tr")
th = html.find_all("th")

gamelist = []

for data in html.find_all("tr"):
    for i, header in enumerate(data.find_all("th", {"rowspan" : 2})):
        if header.text == "Title":
            titleColumn = i

#    dic = {"Title": "", "Comment": ""}
#    temp = str(data.text).split("\n")
#    print(temp)

    #if "Original Title" in temp[1]:
         # Game list starts after this
    #     pass
#    if "Nintendo Entertainment System" in temp[0]:
        # List ends here
#        break


#    dic["Title"] = temp[1]
#    if temp[2] is not "" and temp[2] is not "—" and temp[1] is not temp[2]:
#        dic["Comment"] = "Western title: {}".format(temp[2])

#    gamelist.append(dic)

#for row in gamelist:
#    print(row)