#!/usr/bin/env python

from widgets.tabwidgets import *
from widgets.inputwindow import InputWindow
from widgets.importwindow import ImportWindow
from widgets.overview import Overview

from PySide2.QtWidgets import QMainWindow, QDialog, QTabWidget,\
    QAction, QMenu, QApplication, QMessageBox, QLineEdit, QDesktopWidget
from PySide2.QtGui import QIcon
from PySide2.QtSql import QSqlDatabase

_VERSION = "0.0.13"


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # 'Add to collection' window
        self.addWindow = None

        # 'Import games' window
        self.importWindow = None

        # Tables and their databases
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("data/db/collection.db")
        if not self.db.open():
            QMessageBox.critical(None, "Database Error", self.db.lastError().text())
        self.gamesTableView = Table("games", self.db)
        self.consolesTableView = Table("consoles", self.db)
        self.accessoriesTableView = Table("accessories", self.db)
        self.tableViewList = [self.gamesTableView,
                              self.consolesTableView,
                              self.accessoriesTableView]

        self.overview = Overview(self.tableViewList)

        self.randomizer = Randomizer(self.gamesTableView.ownedItems())
        self.randomizer.consoleList.itemClicked.connect(self.updateStatusbar)
        self.randomizer.btnAll.clicked.connect(self.updateStatusbar)
        self.randomizer.btnNone.clicked.connect(self.updateStatusbar)

        ## MainWindow layout
        # Widgets
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.tab = QTabWidget()

        self.toolbar = self.addToolBar("Exit")
        self.toolbar.addAction(self.buttonActions("exit"))
        self.toolbar.addAction(self.buttonActions("add"))
        self.toolbar.addAction(self.buttonActions("import"))

        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.fileMenu.addAction(self.buttonActions("add"))
        self.fileMenu.addAction(self.buttonActions("open"))
        self.fileMenu.addAction(self.buttonActions("import"))
        self.fileMenu.insertSeparator(self.buttonActions("exit"))
        self.fileMenu.addAction(self.buttonActions("exit"))
        self.viewMenu = self.menuBar().addMenu(self.tr("&View"))
        self.viewMenu.addAction(self.buttonActions("owned"))
        self.viewMenu.addAction(self.buttonActions("delnotowned"))
        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.buttonActions("about"))

        # Search stuff
        self.searchLabel = QLabel("Search")
        self.searchBox = QLineEdit()
        self.searchBox.setEnabled(False)
        self.searchBox.setClearButtonEnabled(True)
        self.searchBox.textChanged.connect(self.search)
        self.advSearchBtn = QPushButton("Advanced search")
        self.advSearchBtn.setToolTip("Doesn't actually work yet")

        # Tab layout.
        self.tab.addTab(self.overview.layout, "Overview")
        self.tab.addTab(self.gamesTableView, "Games")
        self.tab.addTab(self.consolesTableView, "Consoles")
        self.tab.addTab(self.accessoriesTableView, "Accessories")
        self.tab.addTab(self.randomizer.layout, "Randomizer")
        self.tab.currentChanged.connect(self.search)
        self.tab.currentChanged.connect(self.updateStatusbar)

        self.tabGrid = QGridLayout()
        self.tabGrid.setMargin(0)
        self.tabGrid.setSpacing(0)
        self.tabGrid.addWidget(self.tab, 0, 1, 1, 3)
        self.tabGrid.addWidget(self.searchLabel, 1, 1)
        self.tabGrid.addWidget(self.searchBox, 1, 2)
        self.tabGrid.addWidget(self.advSearchBtn, 1, 3)
        self.tabWidget = QWidget()
        self.tabWidget.setLayout(self.tabGrid)

        # Grid layout where we put everything
        self.mainGrid = QGridLayout()
        self.mainGrid.setMargin(0)
        self.mainGrid.setSpacing(0)
        self.mainGrid.addWidget(self.tabWidget, 0, 0)

        # Main layout
        self.centralWidget.setLayout(self.mainGrid)
        gSize = QApplication.desktop().availableGeometry()
        if gSize.width() <= 1280 or gSize.height() <= 768:
            self.showMaximized()
        else:
            self.resize(1280, 768)
            self.center()
        self.setWindowTitle("Game Collection Manager v{}".format(_VERSION))
        self.show()

        self.statusBar().showMessage("")

    def about(self):
        aboutMsg = QMessageBox()
        aboutMsg.setIcon(QMessageBox.Information)
        aboutMsg.setWindowTitle("About")
        aboutMsg.setText("<h2>Game Collection Manager</h2>")
        aboutMsg.setInformativeText("Version {}\n".format(_VERSION))
        aboutMsg.exec_()
        self.updateStatusbar()

    def addToCollection(self):
        """
        Adds data to the collection using InputWindow
        """

        # Get all the platforms in the collection for InputWindow's platform spinbox
        platforms = set()
        platforms |= self.gamesTableView.platforms()
        platforms |= self.consolesTableView.platforms()
        platforms |= self.accessoriesTableView.platforms()

        # Loop until user enters valid data
        while True:
            self.addWindow = InputWindow(sorted(platforms, key=str.lower))
            if self.addWindow.exec_() == QDialog.Accepted:
                data = self.addWindow.returnData()

                if "Game" in data.keys() and data['Name'] is not "":
                    self.gamesTableView.addData(data)
                    self.tab.setCurrentIndex(1)
                elif "Console" in data.keys() and data['Name'] is not "":
                    self.consolesTableView.addData(data)
                    self.tab.setCurrentIndex(2)
                elif "Accessory" in data.keys() and data['Name'] is not "":
                    self.accessoriesTableView.addData(data)
                    self.tab.setCurrentIndex(3)
                else:
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setWindowTitle("Invalid name")
                    msgBox.setText("Name cannot be empty")
                    msgBox.exec_()
                    continue
            break

    def deleteFromCollection(self):
        currentTab = self.tab.currentIndex()

        if 0 < currentTab < 4:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Delete items")
            msgBox.setText("Are you sure?")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            ok = msgBox.exec_()

            if ok == QMessageBox.Ok:
                rows = []
                indexes = self.tableViewList[currentTab-1].selectedIndexes()
                for index in indexes:
                    rows.append(index.row())
                self.tableViewList[currentTab-1].deleteData(rows)

    def deleteNotOwned(self):
        """
        Deletes items in table that are not owned. Not owned items are items that
        don't have either the item itself, the box, or the manual.
        """
        currentTab = self.tab.currentIndex()

        if 0 < currentTab < 4:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Remove not owned items")
            msgBox.setText("Are you sure?")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            ok = msgBox.exec_()

            if ok == QMessageBox.Ok:
                self.tableWidgetList[currentTab-1].deleteNotOwned()

    def importToDatabase(self):
        """
        Imports all games from selected platforms into database as not owned.
        This is to make it easier for the user to quickly go through the games
        in a platform and check which games they own.
        """
        self.importWindow = ImportWindow()
        if self.importWindow.exec_() == QDialog.Accepted:
            data = self.importWindow.returnData()
            self.gamesTableView.addData(data)

    # noinspection PyCallByClass,PyTypeChecker
    def buttonActions(self, action):
        addAct = QAction(QIcon().fromTheme("document-new"), "&Add to collection", self)
        addAct.setShortcut("Ctrl+A")
        addAct.setToolTip("Add to collection")
        addAct.triggered.connect(self.addToCollection)

        delText = "&Delete row"

        currentTab = self.tab.currentIndex()
        if 0 < currentTab < 4:
            if len(self.tableViewList[currentTab-1].selectedIndexes()) > 1:
                delText += "s"
        delAct = QAction(QIcon().fromTheme("edit-delete"), delText, self)
        delAct.setToolTip("Delete from collection")
        delAct.triggered.connect(self.deleteFromCollection)

        opnAct = QAction(QIcon.fromTheme("document-open"), "&Open csv file", self)
        opnAct.setShortcut("Ctrl+O")
        opnAct.setToolTip("Open a csv file for reading")

        savAct = QAction(QIcon.fromTheme("document-save"), "&Save tables", self)
        savAct.setShortcut("Ctrl+S")
        savAct.setToolTip("Saves the tables to the database")

        impAct = QAction(QIcon.fromTheme("list-add"), "&Import games to database", self)
        impAct.setShortcut("Ctrl+I")
        impAct.setToolTip("Import games to database")
        impAct.triggered.connect(self.importToDatabase)

        ownAct = QAction("Hide games not in collection", self)
        ownAct.setCheckable(True)
        ownAct.setChecked(True)
        ownAct.triggered.connect(self.toggleOwnedFilter)

        delNotOwned = QAction(QIcon().fromTheme("edit-delete"), "Remove items not in collection", self)
        delNotOwned.setToolTip("Remove items that are not owned from database")
        delNotOwned.triggered.connect(self.deleteNotOwned)

        aboutAct = QAction(QIcon.fromTheme("help-about"), "Abou&t", self)
        aboutAct.setToolTip("About Game Collection Manager")
        aboutAct.triggered.connect(self.about)

        exitAct = QAction(QIcon.fromTheme("application-exit"), "&Exit", self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.setToolTip("Exit application")
        exitAct.triggered.connect(self.close)

        act = {"add": addAct, "del": delAct, "open": opnAct, "import": impAct,
               "owned": ownAct, "delnotowned": delNotOwned,
               "about": aboutAct, "exit": exitAct}

        return act.get(action)

    def center(self):
        """Centers window on screen"""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def contextMenuEvent(self, event):
        """Re-implements context menu functionality for our needs."""
        cmenu = QMenu(self)

        currentTab = self.tab.currentIndex()

        addAct = cmenu.addAction(self.buttonActions("add"))
        if 0 < currentTab < 4:
            delAct = cmenu.addAction(self.buttonActions("del"))
        opnAct = cmenu.addAction(self.buttonActions("open"))
        exitAct = cmenu.addAction(self.buttonActions("exit"))
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        self.updateStatusbar()

    def search(self):
        """Filters table contents based on user input"""

        currentTab = self.tab.currentIndex()
        searchText = self.searchBox.text()

        if 0 < currentTab < 4:
            self.searchBox.setEnabled(True)
            self.tableViewList[currentTab - 1].filterTable(searchText)
            if searchText is not "":
                self.statusBar().showMessage("Found {} {}.".format(self.tableViewList[currentTab-1].model.rowCount(),
                                                                   self.tableViewList[currentTab-1].model.tableName()))
            else:
                self.updateStatusbar()
        else:
            self.searchBox.setEnabled(False)

    def toggleOwnedFilter(self):
        for table in self.tableViewList:
            table.setHideNotOwned(False) if table.hideNotOwned\
                else table.setHideNotOwned(True)
        currentTab = self.tab.currentIndex()
        if 0 < currentTab < 4:
            self.tableViewList[currentTab-1].filterTable(self.searchBox.text())
            self.tableViewList[currentTab-1].resizeRowsToContents()
        self.updateStatusbar()

    def updateStatusbar(self):
        currentTab = self.tab.currentIndex()
        itemType = ["games", "consoles", "accessories"]

        if currentTab == 0:
            self.statusBar().showMessage("")
        elif 0 < currentTab < 4:
            numItems = self.tableViewList[currentTab-1].ownedCount()
            if self.tableViewList[currentTab-1].hideNotOwned:
                self.statusBar().showMessage("{} {} in collection.".format(numItems, itemType[currentTab-1]))
            else:
                self.statusBar().showMessage("Showing {} {} ({} {} in collection).".format(
                    self.tableViewList[currentTab-1].model.rowCount(),  # TODO: Only shows currently loaded rows
                    itemType[currentTab-1],
                    numItems,
                    itemType[currentTab-1]))
        elif currentTab == 4:
            platforms = self.randomizer.consoleList.selectedItems()
            self.statusBar().showMessage("Select platforms to randomize from.")
            if len(platforms) > 0:
                self.statusBar().showMessage("Selecting from {} games.".format(self.randomizer.getGameCount()))
            return
