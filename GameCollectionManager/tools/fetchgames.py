#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

url = "file:///home/synt4x/Code/Projects/GameCollectionManager/" +\
    "GameCollectionManager/data/html/PS1-AL.html"

rawHTML = urlopen(url)
html = bs(rawHTML, "html.parser")

titleColumn = 0
jpReleaseColumn = 3
euReleaseColumn = 4
naReleaseColumn = 5

tr = html.find_all("tr")
td = []

for row in tr:
    td.append(row.find_all("td"))

stop = False
for entry in td:
    if stop == True:
        break
    for row in entry:
        if row.text == "Home consoles":
            stop = True
            break
        print(row.text)

gamelist = []

#for data in html.find_all("tr"):
#    for i, header in enumerate(data.find_all("td", {""})):


#print (titleColumn, jpReleaseColumn, euReleaseColumn, naReleaseColumn)



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
