#!/usr/bin/env python

import csv
import sqlite3

con = sqlite3.connect("collection.db")
cur = con.cursor()
cur.execute('CREATE TABLE games (ID, Platform, Name, Region, Code, Game, Box, Manual, Year, Comment);')
cur.execute('CREATE TABLE consoles (ID, Platform, Name, Region, Country, "Serial number", Console, Box, Manual, Year, Comment);')
cur.execute('CREATE TABLE accessories (ID, Platform, Name, Region, Country, Accessory, Box, Manual, Year, Comment);')

with open("gamesdb.tsv", 'r', encoding='utf8') as f:
    dr = csv.DictReader(f, dialect="excel-tab")
    to_games = [(i["ID"], i["Platform"], i["Name"], i["Region"], i["Code"],
                 i["Game"], i["Box"], i["Manual"], i["Year"], i["Comment"])
                for i in dr]

with open("consolesdb.tsv", 'r', encoding='utf8') as f:
    dr = csv.DictReader(f, dialect="excel-tab")
    to_consoles = [(i["ID"], i["Platform"], i["Name"], i["Region"], i["Country"],
                    i["Serial number"], i["Console"], i["Box"], i["Manual"],
                    i["Year"], i["Comment"])
                   for i in dr]

with open("accessoriesdb.tsv", 'r', encoding='utf8') as f:
    dr = csv.DictReader(f, dialect="excel-tab")
    to_accessories = [(i["ID"], i["Platform"], i["Name"], i["Region"], i["Country"],
                       i["Accessory"], i["Box"], i["Manual"], i["Year"], i["Comment"])
                      for i in dr]

cur.executemany('INSERT INTO games (ID, Platform, Name, Region, Code, Game, Box, Manual, Year, Comment)'
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', to_games)
cur.executemany('INSERT INTO consoles (ID, Platform, Name, Region, Country, "Serial number", Console, Box, Manual, Year, Comment)'
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', to_consoles)
cur.executemany('INSERT INTO accessories (ID, Platform, Name, Region, Country, Accessory, Box, Manual, Year, Comment)'
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', to_accessories)

con.commit()
con.close()
