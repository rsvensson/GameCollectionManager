#!/usr/bin/env python

"""
Converts a plain text games list from vgdb.io
into csv data that can be used with GCM.
"""

from collections import OrderedDict


def _readTextFile(infile):
    try:
        with open(infile, 'r', encoding='utf8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError("No such file: {}".format(infile))

    if len(lines) == 0:
        raise IOError("File {} is empty!".format(infile))

    gamedata = []

    # Extract the info we want
    for i, line in enumerate(lines):
        if "|" not in line:
            raise TypeError("Line {} in file {} is missing '|' delimiters.".format(i, infile))
        else:
            temp = line.split("|")

        if len(temp) is not 7:
            raise TypeError("Line {} in file {} malformed:\n{}".format(i, infile, temp))
        else:
            for i, row in enumerate(temp):
                temp[i] = row.strip()
            gamedata.append({"Name": temp[2],
                             "Platform": temp[4],
                             "Region": temp[6],
                             "Year": temp[5]})

    return gamedata


def createGameData(infile):
    filedata = _readTextFile(infile)
    gamedata = []

    for game in filedata:
        gamedata.append(OrderedDict({"Platform": game["Platform"], "Name": game["Name"],
                                     "Region": game["Region"], "Code": "",
                                     "Game": "No", "Box": "No",
                                     "Manual": "No", "Year": game["Year"],
                                     "Comment": ""}))

    return gamedata
