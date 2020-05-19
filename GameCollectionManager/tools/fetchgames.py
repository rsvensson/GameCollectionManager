#!/usr/bin/env python

from urllib.request import urlopen

from bs4 import BeautifulSoup as bs


def parse_html_table(table):
    games = []

    for row in table.find_all("tr"):
        columns = row.find_all("pre")
        code = ""
        name = ""
        for column in columns:
            a = column.find("a")
            if a is not None:
                code = a.text.strip()
            elif a is None and column is not None and column.text.strip() != "NTSC-J":
                name = column.text.strip()

        if len(code) > 0 and len(name) > 0:
            games.append({"Name": name, "Code": code})

    return games


def parse_url(adress):
    response = urlopen(adress)
    soup = bs(response, "html.parser")
    table = soup.find("table", {"style": "border-collapse: collapse"})
    return parse_html_table(table)


def writeToDat(datFileName, games, platform, region):
    try:
        with open(datFileName, "w", encoding="utf8") as f:
            for game in games:
                line = "| | {} | | {} | | {} | {}\n".format(game["Name"], platform, region, game["Code"])
                f.write(line)
    except Exception as e:
        print("Error: " + str(e))


url = "file:///home/synt4x/Code/Projects/GameCollectionManager/" +\
    "GameCollectionManager/data/html/PS1JP.html"
# url = "https://web.archive.org/web/20150408124919/http://www.sonyindex.com/Pages/PSone_US_Name.htm"

gamelist = parse_url(url)

writeToDat("PS1JP.dat", gamelist, "Playstation", "Japan")
