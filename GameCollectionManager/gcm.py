#!/usr/bin/env python
import sys
import platform
#import qtmodern.windows
#import qtmodern.styles
#from qtpy.QtWidgets import QApplication
from PySide2.QtWidgets import QApplication
from GameCollectionManager.widgets.mainwindow import MainWindow


def detectPlatform() -> dict:
    return dict(system=platform.system(), release=platform.release())


def createWindow():
    OS = detectPlatform()
    app = QApplication(sys.argv)
    win = MainWindow()

    if OS["system"] == "Windows":
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet(True))

    win.show()
    sys.exit(app.exec_())


def main():
    createWindow()


if __name__ == "__main__":
    main()
