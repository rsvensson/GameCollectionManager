#!/usr/bin/env python

import csv
from pathlib import Path
from sys import argv, exit

if len(argv) < 5:
    scriptFile = Path(argv[0]).name
    print("{}:".format(scriptFile),
          "Takes a column name and value, and puts it after a specified column.\n\n",
          "Usage: {} {} {} {} {}".format(scriptFile, "<column name>",
                                         "<value>", "<column to insert after>",
                                         "<path to csv file>"))
    exit()

columnName = argv[1]
value = argv[2]
afterColumn = argv[3]
filename = Path(argv[4])

data = []

with filename.open('r', encoding='utf8') as f:
    reader = csv.DictReader(f, dialect="excel-tab")
    for row in reader:
        data.append(row)

for row in data:
    newData = row.__class__()
    for key, val in row.items():
        if key == "Owned":
            continue
        newData[key] = val
        if key == afterColumn:
            newData[columnName] = value

    row.clear()
    row.update(newData)

with filename.open('w', encoding='utf8') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys(), dialect="excel-tab")
    writer.writeheader()
    writer.writerows(data)

print("Done")
