#!/usr/bin/env python

"""
Converts a plain text games list from vgdb.io
into csv data that can be used with GCM.
"""

from sys import argv, exit
from pathlib import Path
import csv


def readTextFile(infile):
    try:
        with open(infile, 'r', encoding='utf8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("No such file: {}\nAborting.")
        exit(2)

    if len(lines) == 0:
        print("Input file is empty! Aborting.")
        exit(3)

    gamedata = []

    # Extract the info we want
    for i, line in enumerate(lines):
        if "|" not in line:
            print("Line {} in input file is not a valid VGDB.io text file (e.g it doesn't have any '|' characters):".format(i))
            print(line + "\n")
            print("Example line from a valid text file:")
            print("|       | Battlezone                 | Atari, Inc. | Atari 2600 | 1983 | Japan")
            exit(4)

        temp = line.split("|")

        if len(temp) is not 7:
            print("Line {} in input file malformed:".format(i))
            print(line + "\n")
            print("Example line from a valid text file:")
            print("|       | Battlezone                 | Atari, Inc. | Atari 2600 | 1983 | Japan")
            print("(Whitespace is not important, but it must consist of six segments separated by '|' characters.")
            exit(5)

        for i, row in enumerate(temp):
            temp[i] = row.strip()
        gamedata.append({"Name": temp[2],
                         "Platform": temp[4],
                         "Region": temp[6],
                         "Year": temp[5]})

    return gamedata


def createCSV(gamedata, outfile):
    dialect = "excel-tab" if outfile.suffix[1:] == "tsv" else "excel"

    with open(outfile, 'w', encoding='utf8') as f:
        headers = ["Platform", "Name", "Region", "Code", "Game", "Box", "Manual", "Year", "Comment"]
        writer = csv.DictWriter(f, fieldnames=headers, dialect=dialect)
        writer.writeheader()

        for game in gamedata:
            row = {"Platform": game["Platform"], "Name": game["Name"],
                   "Region": game["Region"], "Code": "",
                   "Game": "No", "Box": "No",
                   "Manual": "No", "Year": game["Year"],
                   "Comment": ""}
            writer.writerow(row)


def main():
    if len(argv) <= 2:
        print("{}: Converts a vgdb.io plain text game list into csv format\n".format(Path(argv[0]).name))
        print("Usage: {} <input file (.txt)> <output file (.csv/.tsv)>".format(Path(argv[0]).name))
        exit()

    infile = Path(argv[1])
    outfile = Path(argv[2])
    if outfile.suffix[1:] not in ["csv", "tsv"]:
        print("Invalid output file suffix. Only '.csv' and '.csv' allowed.")
        exit(1)

    createCSV(readTextFile(infile), outfile)


if __name__ == "__main__":
    main()
