#!/usr/bin/env python
import os
import sys
import platform
from PySide2.QtWidgets import QApplication
from widgets.mainwindow import MainWindow


def createWindow(dbPath):
    #OS = detectPlatform()
    app = QApplication(sys.argv)
    win = MainWindow(dbPath)

    #if OS["system"] == "Windows":
    #    import qdarkstyle
    #    app.setStyleSheet(qdarkstyle.load_stylesheet(True))

    win.show()
    sys.exit(app.exec_())


def createDB(dbpath):
    import sqlite3
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS games "
                "(ID int, Platform, Name, Region, Code, Game, Box, Manual, Year, Comment);")
    cur.execute("CREATE TABLE IF NOT EXISTS consoles "
                "(ID int, Platform, Name, Region, Country, 'Serial number', Console, Box, Manual, Year, Comment);")
    cur.execute("CREATE TABLE IF NOT EXISTS accessories "
                "(ID int, Platform, Name, Region, Country, Accessory, Box, Manual, Year, Comment);")
    con.commit()
    con.close()


def detectPlatform() -> dict:
    return dict(system=platform.system(), release=platform.release())


def getScriptDir(followSymlinks=True):
    #if getattr(sys, 'frozen', False):  # py2exe, PyInstaller, cx_freeze
    #    path = os.path.abspath(sys.executable)
    #else:
    import inspect
    path = inspect.getabsfile(getScriptDir)
    if followSymlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


def main():
    # TODO: Doesn't create collection.db if only the file is missing
    # TODO: Issue with dynamically created dbs where it removes items that are in collection
    gcmDir = getScriptDir()
    dbPath = gcmDir+"/data/db/collection.db"

    if not os.path.exists(gcmDir+"/data"):
        os.makedirs(gcmDir+"/data/db")
        os.mkdir(gcmDir+"/data/vgdb")
        createDB(dbPath)
    elif not os.path.exists(gcmDir+"/data/db"):
        os.mkdir(gcmDir+"/data/db")
        if not os.path.exists(gcmDir+"/data/vgdb"):
            os.mkdir(gcmDir+"/data/vgdb")
        createDB(dbPath)

    createWindow(dbPath)


if __name__ == "__main__":
    main()
