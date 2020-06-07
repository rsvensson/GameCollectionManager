#!/usr/bin/env python

"""
Converts a plain text games list from vgdb.io
into csv data that can be used with GCM.
"""


def _readTextFile(infile):
    try:
        with open(infile, 'r', encoding='utf8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"No such file: {infile}")

    if len(lines) == 0:
        raise IOError(f"File {infile} is empty!")

    gamedata = []

    # Extract the info we want
    for i, line in enumerate(lines):
        if "|" not in line:
            raise TypeError(f"Line {i} in file {infile} is missing '|' delimiters.")
        else:
            temp = line.split("|")

        if 6 < len(temp) < 9:
            for j, row in enumerate(temp):
                temp[j] = row.strip()
            if len(temp) == 7:
                gamedata.append({"name": temp[2],
                                 "platform": temp[4],
                                 "region": temp[6],
                                 "year": temp[5],
                                 "code": ""})
            elif len(temp) == 8:
                gamedata.append({"name": temp[2],
                                 "platform": temp[4],
                                 "region": temp[6],
                                 "year": "",
                                 "code": temp[7]})
        else:
            raise TypeError(f"Line {i} in file {infile} malformed:\n{temp}")

    return gamedata


def createGameData(infile):
    filedata = _readTextFile(infile)
    gamedata = []

    for game in filedata:
        gamedata.append({"platform": game["platform"], "name": game["name"],
                         "region": game["region"], "code": game["code"],
                         "game": "No", "box": "No", "manual": "No",
                         "year": game["year"], "genre": "", "comment": "",
                         "publisher": "", "developer": "", "platforms": ""})

    return gamedata
