#!/usr/bin/env python

import csv
import sqlite3

con = sqlite3.connect("collection.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS games "
            "(ID INTEGER PRIMARY KEY, Platform, Name, Region, Code, Game, Box, Manual, Year, Genre, Comment, "
            "Publisher, Developer, Platforms, Price);")
cur.execute("CREATE TABLE IF NOT EXISTS consoles "
            "(ID INTEGER PRIMARY KEY, Platform, Name, Region, Country, 'Serial number', Console, Box, Manual, "
            "Year, Comment, Price);")
cur.execute("CREATE TABLE IF NOT EXISTS accessories "
            "(ID INTEGER PRIMARY KEY, Platform, Name, Region, Country, Accessory, Box, Manual, Year,"
            "Comment, Price);")

with open("games.tsv", 'r', encoding='utf8') as f:
    dr = csv.DictReader(f, dialect="excel-tab")
    to_games = [(i["ID"], i["Platform"], i["Name"], i["Region"], i["Code"],
                 i["Game"], i["Box"], i["Manual"], i["Year"], i["Genre"], i["Comment"],
                 i["Publisher"], i["Developer"], i["Platforms"], i["Price"])
                for i in dr]

with open("consoles.tsv", 'r', encoding='utf8') as f:
    dr = csv.DictReader(f, dialect="excel-tab")
    to_consoles = [(i["ID"], i["Platform"], i["Name"], i["Region"], i["Country"],
                    i["Serial number"], i["Console"], i["Box"], i["Manual"],
                    i["Year"], i["Comment"], i["Price"])
                   for i in dr]

with open("accessories.tsv", 'r', encoding='utf8') as f:
    dr = csv.DictReader(f, dialect="excel-tab")
    to_accessories = [(i["ID"], i["Platform"], i["Name"], i["Region"], i["Country"],
                       i["Accessory"], i["Box"], i["Manual"], i["Year"], i["Comment"], i["Price"])
                      for i in dr]

cur.executemany('INSERT INTO games (ID, Platform, Name, Region, Code, Game, Box, Manual, Year, Genre, Comment, '
                'Publisher, Developer, Platforms, Price)'
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', to_games)
cur.executemany('INSERT INTO consoles (ID, Platform, Name, Region, Country, "Serial number", Console, Box, Manual, '
                'Year, Comment, Price) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', to_consoles)
cur.executemany('INSERT INTO accessories (ID, Platform, Name, Region, Country, Accessory, Box, Manual, Year, Comment, '
                'Price)'
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', to_accessories)

con.commit()
con.close()
