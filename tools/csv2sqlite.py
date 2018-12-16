#!/usr/bin/env python

import csv
import sqlite3

con = sqlite3.connect("games.db")
cur = con.cursor()
cur.execute("CREATE TABLE games (Platform, Name, Region, Code, Game, Box, Manual, Year, Comment);")

with open("gamesdb.tsv", 'r', encoding='utf8') as f:
    dr = csv.DictReader(f, dialect="excel-tab")
    to_db = [(i["Platform"], i["Name"], i["Region"], i["Code"],
             i["Game"], i["Box"], i["Manual"], i["Year"], i["Comment"])
             for i in dr]

cur.executemany("INSERT INTO games (Platform, Name, Region, Code, Game, Box, Manual, Year, Comment)"
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()
