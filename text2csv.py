#!/usr/bin/env python

"""
Converts the plain text games lists from vgdb.io
into csv data that can be used with GCM.
"""

from sys import argv
import csv


def readTextFile(infile):
    with open(infile, 'r', encoding='utf8') as f:
        rows = f.readlines()

    games = []

    # Extract the info we want
    for row in rows:
        temp = row.split("|")
        for i, r in enumerate(temp):
            temp[i] = r.strip()
        games.append(temp[2])

    return games


def createCSV(data, outfile, platform, region):
    with open(outfile, 'w', encoding='utf8') as f:
        headers = ["Platform", "Name", "Region", "Code", "Game", "Box", "Manual", "Comment"]
        writer = csv.DictWriter(f, fieldnames=headers, dialect="excel-tab")
        writer.writeheader()

        for name in data:
            row = {"Platform": platform, "Name": name,
                   "Region": region, "Code": "",
                   "Game": "No", "Box": "No",
                   "Manual": "No", "Comment": ""}
            writer.writerow(row)


def main():
    output = readTextFile(argv[1])

    outfile = argv[2]
    platform = argv[3]
    region = argv[4]

    createCSV(output, outfile, platform, region)


if __name__ == "__main__":
    main()
