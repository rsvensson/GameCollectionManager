#!/usr/bin/env python

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen


class TableParser:
    def parse_url(self, url):
        response = urlopen(url)
        soup = bs(response, "html.parser")
        table = soup.find("table", {"style":"border-collapse: collapse"})
        return self.parse_html_table(table)

    def parse_html_table(self, table):
        gamelist = []

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
                gamelist.append({"Name": name, "Code": code})

        return gamelist


def writeToDat(datFileName, gamelist, platform, region):
    try:
        with open(datFileName, "w", encoding="utf8") as f:
            for game in gamelist:
                line = "| | {} | | {} | | {} | {}\n".format(game["Name"], platform, region, game["Code"])
                f.write(line)
    except Exception as e:
        print("Error: " + str(e))



url = "file:///home/synt4x/Code/Projects/GameCollectionManager/" +\
    "GameCollectionManager/data/html/PS1JP.html"
#url = "https://web.archive.org/web/20150408124919/http://www.sonyindex.com/Pages/PSone_US_Name.htm"

tp = TableParser()
gamelist = tp.parse_url(url)

writeToDat("PS1JP.dat", gamelist, "Playstation", "Japan")
