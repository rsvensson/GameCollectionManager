#!/usr/bin/env python

import csv

class Database:
    """Database for game collection. Handles csv or tsv files.
       Should be able to handle any amount of fieldnames."""

    def __init__(self, file):
        """file: pathlib Path object"""

        self._file = file
        self._path = file.parent
        self._suff = file.suffix
        self._data = []  # List where we will store our OrderedDicts
        self._dial = "excel-tab" if self._suff == ".tsv" else "excel"

        if self._suff == ".tsv" or self._suff == ".csv":
            self._refreshData()
        else:
            raise TypeError("Only .csv and .tsv files supported")


    def _refreshData(self):
        """Reads data from csv file and puts it into our OrderedDict data structure"""

        self._data.clear()

        try:
            with self._file.open('r', encoding='utf8') as f:
                csvData = csv.DictReader(f, dialect=self._dial)
                for row in csvData:
                    self._data.append(row)
        except FileNotFoundError:  # Handle non-existing database files with some defaults
            self._path.mkdir(parents=True, exist_ok=True)
            fields = []
            if "game" in self._file.name:
                fields = ["Platform,Name,Region,Code,Cart,Box,Manual,Year,Comment"] if self._suff == ".csv"\
                    else ["Platform\tName\tRegion\tCode\tCart\tBox\tManual\tYear\tComment"]
            elif "console" in self._file.name:
                fields = ["Platform,Name,Region,Country,Serial number,Box,Manual,Comment"] if self._suff == ".csv"\
                    else ["Platform\tName\tRegion\tCountry\tSerial number\tConsole\tBox\tManual\tComment"]
            elif "accessor" in self._file.name:
                fields = ["Platform,Name,Region,Country,Accessory,Box,Manual,Comment"] if self._suff == ".csv"\
                    else ["Platform\tName\tRegion\tCountry\tAccessory\tBox\tManual\tComment"]
            with self._file.open('x', encoding='utf8') as f:
                f.writelines(fields)

            self._refreshData()
        except Exception as e:
            print("Error: " + str(e))

    def _sortFile(self):
        """Since we can't reorder a list of OrderedDicts, which is what's in
           self._data, after we saved the data with our saveData method we have
           to open the file as a regular file and sort it manually that way.
           There must be a better way of doing this..."""
        try:
            with open(self._file, 'r', encoding='utf8') as f:
                temp = f.readlines()
        except Exception as e:
            print("Error: " + str(e))
            return

        # Separate the keys and data so we don't sort the keys
        data = temp[1:]
        data.sort(key=str.lower)  # Make sure to use str.lower because the tablewidget sure does...

        try:
            with self._file.open('w', encoding="utf8") as f:
                f.writelines(temp[0])
                f.writelines(data)
        except Exception as e:
            print("Error: " + str(e))
            return

    def connect(self):
        return self._data

    def saveData(self, newData):
        fields = []
        if len(newData) > 0:
            fields = list(newData[0].keys())
        else:  # Handles case where user deletes everything in collection
            if "game" in self._file.name:
                fields = ["Platform", "Name", "Region", "Code", "Cart", "Box", "Manual", "Year", "Comment"]
            elif "console" in self._file.name:
                fields = ["Platform", "Name", "Region", "Country", "Serial number", "Console", "Box", "Manual", "Comment"]
            elif "accessor" in self._file.name:
                fields = ["Platform", "Name", "Region", "Country", "Accessory", "Box", "Manual", "Comment"]

        try:
            with self._file.open('w', encoding="utf8") as f:
                writer = csv.DictWriter(f, fieldnames=fields, dialect=self._dial)
                writer.writeheader()
                if len(newData) > 0:
                    for row in newData:
                        writer.writerow(row)
        except Exception as e:
            print("Error: " + str(e))
            return

        # Sort the file after saving it then refresh current data
        self._sortFile()
        self._refreshData()
