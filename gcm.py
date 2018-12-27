#!/usr/bin/env python
import sys
from PySide2.QtWidgets import QApplication
from widgets.mainwindow import MainWindow


def createWindow():
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())


def main():
    createWindow()


if __name__ == "__main__":
    main()
