#!/usr/bin/env python

from pathlib import Path
from widgets.mainwindow import createWindow


def main():
    gamesDBPath = Path("data/db/gamesdb.tsv")
    consolesDBPath = Path("data/db/consolesdb.tsv")
    accessoriesDBPath = Path("data/db/accessoriesdb.tsv")

    createWindow(gamesDBPath, consolesDBPath, accessoriesDBPath)


if __name__ == "__main__":
    main()
