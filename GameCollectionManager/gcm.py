#!/usr/bin/env python
import os
import platform
import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QColor
from PySide2.QtWidgets import QApplication
from widgets.mainwindow import MainWindow


def createWindow(dbPath):
    #OS = detectPlatform()
    app = QApplication(sys.argv)
    setPalette(app)
    win = MainWindow(dbPath)

    win.show()
    sys.exit(app.exec_())


def createDB(dbpath):
    import sqlite3
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS games "
                "(ID INTEGER PRIMARY KEY, Platform, Name, Region, Code, Game, Box, Manual, Year, Genre, Comment, Publisher, Developer, Platforms);")
    cur.execute("CREATE TABLE IF NOT EXISTS consoles "
                "(ID INTEGER PRIMARY KEY, Platform, Name, Region, Country, 'Serial number', Console, Box, Manual, Year, Comment);")
    cur.execute("CREATE TABLE IF NOT EXISTS accessories "
                "(ID INTEGER PRIMARY KEY, Platform, Name, Region, Country, Accessory, Box, Manual, Year, Comment);")
    con.commit()
    con.close()


def detectPlatform() -> dict:
    return dict(system=platform.system(), release=platform.release())


def getScriptDir(followSymlinks=True):
    if getattr(sys, 'frozen', False):  # py2exe, PyInstaller, cx_freeze
        path = os.path.abspath(sys.executable)
    else:
        import inspect
        path = inspect.getabsfile(getScriptDir)
    if followSymlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


def setPalette(app):
    darkPalette = QPalette()
    darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.WindowText, Qt.white)
    darkPalette.setColor(QPalette.Base, QColor(25, 25, 25))
    darkPalette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
    darkPalette.setColor(QPalette.ToolTipText, Qt.white)
    darkPalette.setColor(QPalette.Text, Qt.white)
    darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ButtonText, Qt.white)
    darkPalette.setColor(QPalette.BrightText, Qt.red)
    darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.HighlightedText, Qt.black)
    darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    darkPalette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)

    app.setStyle("Fusion")
    app.setPalette(darkPalette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")


def main():
    gcmDir = getScriptDir()
    dbPath = gcmDir+"/data/db/collection.db"

    # Make sure we have everything
    if not os.path.exists(gcmDir+"/data"):
        os.makedirs(gcmDir+"/data/db")
        os.mkdir(gcmDir+"/data/vgdb")
        createDB(dbPath)
    if not os.path.exists(gcmDir+"/data/db"):
        os.mkdir(gcmDir+"/data/db")
        createDB(dbPath)
    if not os.path.exists(gcmDir+"/data/vgdb"):
        os.mkdir(gcmDir+"/data/vgdb")
    if not os.path.exists(dbPath):
        createDB(dbPath)

    createWindow(dbPath)


if __name__ == "__main__":
    main()
