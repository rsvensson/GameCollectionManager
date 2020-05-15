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

        if 6 < len(temp) < 9:
            for j, row in enumerate(temp):
                temp[j] = row.strip()
            if len(temp) == 7:
                gamedata.append({"Name": temp[2],
                                 "Platform": temp[4],
                                 "Region": temp[6],
                                 "Year": temp[5],
                                 "Code": ""})
            elif len(temp) == 8:
                gamedata.append({"Name": temp[2],
                                 "Platform": temp[4],
                                 "Region": temp[6],
                                 "Year": "",
                                 "Code": temp[7]})
        else:
            raise TypeError(f"Line {i} in file {infile} malformed:\n{temp}")

    return gamedata


def createGameData(infile):
    filedata = _readTextFile(infile)
    gamedata = []

    for game in filedata:
        gamedata.append(OrderedDict({"Platform": game["Platform"], "Name": game["Name"],
                                     "Region": game["Region"], "Code": game["Code"],
                                     "Game": "No", "Box": "No",
                                     "Manual": "No", "Year": game["Year"],
                                     "Comment": ""}))

    return gamedata
