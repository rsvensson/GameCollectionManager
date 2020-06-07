#!/usr/bin/env python
from os import path
from time import sleep

import requests
from PySide2.QtGui import QIcon
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from PySide2.QtWidgets import QMainWindow, QDialog, QTabWidget, \
    QAction, QMenu, QApplication, QMessageBox, QLineEdit, QDesktopWidget, \
    QWidget, QLabel, QPushButton, QInputDialog, QProgressBar, QVBoxLayout, QComboBox, QHBoxLayout

from utilities.exportcsv import sql2csv
from utilities.fetchinfo import getMobyRelease
from utilities.steamlibrary import getSteamLibrary
from widgets.importwindow import ImportWindow
from widgets.inputwindow import InputWindow
from widgets.overview import Overview
from widgets.randomizer import Randomizer
from widgets.filterdock import FilterDock
from widgets.sidepanel import SidePanel
from widgets.table import Table

_VERSION = "0.3.6"


class MainWindow(QMainWindow):

    # noinspection PyUnresolvedReferences
    def __init__(self, dbpath):
        super(MainWindow, self).__init__()

        # 'Add to collection' window
        self.addWindow = None

        # 'Import games' window
        self.importWindow = None

        # Side panel
        self.sidePanel = SidePanel()

        # Tables and their databases
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(dbpath)
        if not db.open():
            QMessageBox.critical(None, "Database Error", db.lastError().text())
        self.gamesTableView = Table("games", db)
        self.gamesTableView.doubleClick.connect(self.sidePanel.showDetails)
        self.consolesTableView = Table("consoles", db)
        self.consolesTableView.doubleClick.connect(self.sidePanel.showDetails)
        self.accessoriesTableView = Table("accessories", db)
        self.accessoriesTableView.doubleClick.connect(self.sidePanel.showDetails)
        self.tableViewList = [self.gamesTableView,
                              self.consolesTableView,
                              self.accessoriesTableView]

        self.allPlatforms = set()
        self.allRegions = set()
        self.allGenres = set()
        self.allYears = set()
        for table in self.tableViewList:
            for row in table.ownedItems():
                self.allPlatforms.add(row["platform"])
                self.allRegions.add(row["region"])
                self.allYears.add(row["year"])
                # Split multi-genre entries
                for genre in row["genre"].split(", "):
                    self.allGenres.add(genre)

        self.filterDock = FilterDock(sorted(self.allPlatforms, key=str.lower),
                                     sorted(self.allRegions, key=str.lower),
                                     sorted(self.allGenres, key=str.lower),
                                     sorted(self.allYears, key=str.lower))

        # Overview tab
        self.overview = Overview(self.tableViewList)

        # Randomizer tab
        self.randomizer = Randomizer(self.gamesTableView.ownedItems(),
                                     sorted(self.allPlatforms, key=str.lower),
                                     sorted(self.allGenres, key=str.lower))
        self.randomizer.consoleList.itemClicked.connect(self.updateStatusbar)
        self.randomizer.genreList.itemClicked.connect(self.updateStatusbar)
        self.randomizer.genreMatchExclusiveCB.stateChanged.connect(self.updateStatusbar)
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
        self.fileMenu.addAction(self.buttonActions("export"))
        self.fileMenu.addAction(self.buttonActions("import"))
        self.fileMenu.addAction(self.buttonActions("steam"))
        self.fileMenu.addAction(self.buttonActions("fetch"))
        self.fileMenu.insertSeparator(self.buttonActions("exit"))
        self.fileMenu.addAction(self.buttonActions("exit"))
        self.viewMenu = self.menuBar().addMenu(self.tr("&View"))
        self.viewMenu.addAction(self.buttonActions("owned"))
        self.viewMenu.addAction(self.buttonActions("delnotowned"))
        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.buttonActions("about"))

        self.statusProgressBar = QProgressBar()
        self.statusProgressBar.setMaximumSize(100, 15)
        self.statusProgressBar.setRange(0, 0)
        self.statusProgressBar.setVisible(False)
        self.statusBar().addPermanentWidget(self.statusProgressBar)

        # Search stuff
        self.searchLabel = QLabel("Search")
        self.searchLabel.setVisible(False)
        self.searchBox = QLineEdit()
        self.searchBox.setVisible(False)
        self.searchBox.setClearButtonEnabled(True)
        # self.searchBox.textChanged.connect(self.search)
        self.searchBox.returnPressed.connect(self.search)
        self.searchBtn = QPushButton("Search")
        self.searchBtn.clicked.connect(self.search)
        self.searchBtn.setVisible(False)
        self.filterBtn = QPushButton("Filter")
        self.filterBtn.clicked.connect(self.filterDock.toggleVisibility)
        self.filterBtn.setVisible(False)

        # Tab layout.
        self.tab.addTab(self.overview.widget, "Overview")
        self.tab.addTab(self.gamesTableView, "Games")
        self.tab.addTab(self.consolesTableView, "Consoles")
        self.tab.addTab(self.accessoriesTableView, "Accessories")
        self.tab.addTab(self.randomizer.widget, "Randomizer")
        self.tab.currentChanged.connect(self.search)
        self.tab.currentChanged.connect(self.sidePanel.hideDetails)
        # Connect sidePanel's saved signal to corresponding table's updateData()
        # TODO: Update the sets of platforms and genres properly
        self.sidePanel.saved.connect(self.tableViewList[self.tab.currentIndex()].updateData)
        self.sidePanel.saved.connect(lambda: self.randomizer.updateLists(self.gamesTableView.ownedItems(),
                                                                         sorted(self.allPlatforms, key=str.lower),
                                                                         sorted(self.allGenres, key=str.lower)))

        # Main layout
        self.tabHbox = QHBoxLayout()
        self.tabHbox.addWidget(self.tab, 1)
        self.tabHbox.addWidget(self.sidePanel, 1)
        self.advSearchHbox = QHBoxLayout()
        self.advSearchHbox.addWidget(self.filterDock, 0)
        self.searchHbox = QHBoxLayout()
        self.searchHbox.addWidget(self.searchLabel, 0)
        self.searchHbox.addWidget(self.searchBox, 1)
        self.searchHbox.addWidget(self.filterBtn, 0)
        self.searchHbox.addWidget(self.searchBtn, 0)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.tabHbox, 1)
        self.mainLayout.addLayout(self.advSearchHbox, 0)
        self.mainLayout.addLayout(self.searchHbox, 0)
        self.centralWidget.setLayout(self.mainLayout)

        # Make sure screen geometry is big enough. Otherwise set window to maximized.
        gSize = QApplication.desktop().availableGeometry()
        if gSize.width() <= 1280 or gSize.height() <= 768:
            self.showMaximized()
        else:
            self.resize(1280, 768)
            self.center()

        self.setWindowTitle(f"Game Collection Manager v{_VERSION}")
        self.statusBar().showMessage("")

    def about(self):
        aboutMsg = QMessageBox()
        aboutMsg.setIcon(QMessageBox.Information)
        aboutMsg.setWindowTitle("About")
        aboutMsg.setText("<h2>Game Collection Manager</h2>")
        aboutMsg.setInformativeText(f"Version {_VERSION}\n")
        aboutMsg.exec_()
        self.search()

    def addToCollection(self):
        """
        Adds data to the collection using InputWindow
        """

        # Loop until user enters valid data
        while True:
            self.addWindow = InputWindow()
            if self.addWindow.exec_() == QDialog.Accepted:
                data = self.addWindow.returnData()

                if data['platform'].isspace() or data['name'] == "":
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setWindowTitle("Invalid entry")
                    msgBox.setText("Platform and name cannot be empty")
                    msgBox.exec_()
                    continue

                # Update Platform, Region, Genre, and Year in filter dock if necessary
                if data["platform"] not in self.allPlatforms:
                    self.allPlatforms.add(data["platform"])
                    self.filterDock.updatePlatforms(sorted(self.allPlatforms, key=str.lower))
                if data["region"] not in self.allRegions:
                    self.allRegions.add(data["region"])
                    self.filterDock.updateRegions(sorted(self.allRegions, key=str.lower))
                if data["genre"] not in self.allGenres:
                    self.allGenres.add(data["genre"])
                    self.filterDock.updateGenres(sorted(self.allGenres, key=str.lower))
                if data["year"] not in self.allYears:
                    self.allYears.add(data["year"])
                    self.filterDock.updateYears(sorted(self.allYears, key=str.lower))

                if "game" in data.keys():
                    self.gamesTableView.addData(data)
                    self.overview.updateData(self.gamesTableView)
                    self.randomizer.updateLists(self.gamesTableView.ownedItems(),
                                                sorted(self.allPlatforms, key=str.lower),
                                                sorted(self.allGenres, key=str.lower))
                elif "console" in data.keys():
                    self.consolesTableView.addData(data)
                    self.overview.updateData(self.consolesTableView)
                elif "accessory" in data.keys():
                    self.accessoriesTableView.addData(data)
                    self.overview.updateData(self.accessoriesTableView)
                self.search()
            else:
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
                self.overview.updateData(self.tableViewList[currentTab-1])
                if currentTab == 1:
                    self.randomizer.updateLists(self.gamesTableView.ownedItems(),
                                                sorted(self.allPlatforms, key=str.lower),
                                                sorted(self.allGenres, key=str.lower))
                self.search()

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
                self.tableViewList[currentTab-1].deleteNotOwned()
                self.search()

    def fetchInfo(self):
        """
        Fetches info for all games from MobyGames. Sleeps for 5 seconds
        between game so we don't annoy their servers.
        :return:
        """
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Fetch info for all games")
        msgBox.setText("This will take a long time. Are you sure?")
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel)
        ok = msgBox.exec_()

        if ok == QMessageBox.Ok:
            games = self.gamesTableView.ownedItems()
            for game in games:
                info = getMobyRelease(game["name"], game["platform"], game["region"])
                self.gamesTableView.updateData(info)
                if "image" in info.keys() and info["image"] != "":
                    coverDir = path.join("data", "images", "covers")
                    id = str(game["ID"]) + ".jpg"
                    imageData = requests.get(info["image"]).content

                    if not path.exists(path.join(coverDir, id)):
                        with open(path.join(coverDir, id), "wb") as f:
                            f.write(imageData)

                sleep(5)  # Be nice

    def importToDatabase(self):
        """
        Imports all games from selected platforms into database as not owned.
        This is to make it easier for the user to quickly go through the games
        in a platform and check which games they own.
        """
        self.importWindow = ImportWindow()
        if self.importWindow.exec_() == QDialog.Accepted:
            data, platforms, regions = self.importWindow.returnData()
            self.statusProgressBar.setVisible(True)
            self.gamesTableView.addData(data)
            self.statusProgressBar.setVisible(False)

            for platform in platforms:
                if platform not in self.allPlatforms:
                    self.allPlatforms.add(platform)
                    self.filterDock.updatePlatforms(sorted(self.allPlatforms, key=str.lower))
            for region in regions:
                if region not in self.allRegions:
                    self.allRegions.add(region)
                    self.filterDock.updateRegions(sorted(self.allRegions, key=str.lower))
            self.search()

    def importSteamLibrary(self):
        apiKey, ok = QInputDialog.getText(self, "Import Steam Library", "Enter Steam API Key:")
        if ok and not (apiKey.isspace() or apiKey == ""):
            steamID, ok = QInputDialog.getText(self, "Import Steam Library", "Enter Steam User ID:")
            if ok and not (steamID.isspace() or steamID == ""):
                try:
                    games = getSteamLibrary(apiKey, steamID)
                except (PermissionError, ValueError) as e:
                    msgBox = QMessageBox(QMessageBox.Critical, "Error", "An error occured.")
                    msgBox.setInformativeText(str(e))
                    msgBox.exec_()
                else:
                    if "Steam" not in self.allPlatforms:
                        self.allPlatforms.add("Steam")
                        self.allRegions.add("Steam")
                        self.filterDock.updatePlatforms(sorted(self.allPlatforms, key=str.lower))
                        self.filterDock.updateRegions(sorted(self.allRegions, key=str.lower))
                        self.gamesTableView.addData(games)
                    else:  # Only add games not already in collection
                        existingGames = []
                        query = QSqlQuery()
                        query.exec_("SELECT Name from games WHERE Region='Steam'")
                        while query.next():
                            existingGames.append(query.value(0))

                        for game in games:
                            if game["name"] not in existingGames:
                                self.gamesTableView.addData(game)
                    self.overview.updateData(self.gamesTableView)
                    self.randomizer.updateLists(self.gamesTableView.ownedItems(),
                                                sorted(self.allPlatforms, key=str.lower),
                                                sorted(self.allGenres, key=str.lower))
                    self.search()

    def exportToCSV(self):
        def doexport():
            filetype = filetypes.currentText()
            exportTables = []
            db = self.consolesTableView.model.database()
            if tablesBox.currentIndex() == 0:
                for table in tables[1:]:
                    exportTables.append(table.lower())
            elif tablesBox.currentIndex() == 1:
                exportTables.append("games")
            elif tablesBox.currentIndex() == 2:
                exportTables.append("consoles")
            elif tablesBox.currentIndex() == 3:
                exportTables.append("accessories")

            sql2csv(db, exportTables, filetype)
            exportWindow.close()

        exportWindow = QDialog()

        tables = ["All", "Games", "Consoles", "Accessories"]
        tablesLabel = QLabel("Tables to export")
        tablesBox = QComboBox()
        # tablesBox.addItem(None, text="All")
        tablesBox.addItems(tables)
        tablesLayout = QHBoxLayout()
        tablesLayout.addWidget(tablesLabel)
        tablesLayout.addWidget(tablesBox)

        filetypesLabel = QLabel("Filetype")
        filetypes = QComboBox()
        filetypes.addItems(["csv", "tsv"])
        filetypesLayout = QHBoxLayout()
        filetypesLayout.addWidget(filetypesLabel)
        filetypesLayout.addWidget(filetypes)

        # filenameLabel = QLabel("Filename")
        # filename = QLineEdit()
        # filesLayout = QHBoxLayout()
        # filesLayout.addWidget(filenameLabel)
        # filesLayout.addWidget(filename)

        ok = QPushButton("Ok")
        ok.clicked.connect(doexport)
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(exportWindow.close)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)

        layout = QVBoxLayout()
        layout.addLayout(tablesLayout)
        # layout.addLayout(filesLayout)
        layout.addLayout(filetypesLayout)
        layout.addLayout(buttonLayout)

        exportWindow.setLayout(layout)
        exportWindow.exec_()

    # noinspection PyCallByClass,PyTypeChecker
    def buttonActions(self, action: str) -> QAction:
        addAct = QAction(QIcon().fromTheme("list-add"), "&Add to collection...", self)
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

        detAct = QAction(QIcon.fromTheme("text-x-generic-template"), "Details...", self)
        detAct.setToolTip("Open details side-panel")
        detAct.triggered.connect(self.tableViewList[currentTab-1].rowData)

        expAct = QAction(QIcon.fromTheme("text-x-generic-template"), "&Export as csv...", self)
        expAct.setShortcut("Ctrl+E")
        expAct.setToolTip("Export table as CSV file")
        expAct.triggered.connect(self.exportToCSV)

        # not used
        savAct = QAction(QIcon.fromTheme("document-save"), "&Save tables", self)
        savAct.setShortcut("Ctrl+S")
        savAct.setToolTip("Saves the tables to the database")

        impAct = QAction(QIcon.fromTheme("insert-object"), "&Import platform template...", self)
        impAct.setShortcut("Ctrl+I")
        impAct.setToolTip("Import games to database")
        impAct.triggered.connect(self.importToDatabase)

        stmAct = QAction(QIcon.fromTheme("insert-object"), "Import Steam Library...", self)
        stmAct.triggered.connect(self.importSteamLibrary)

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

        infoAct = QAction("Debug: Print row info", self)
        infoAct.triggered.connect(self.info)

        fetchAct = QAction("Fetch info for all games...", self)
        fetchAct.setToolTip("Tries to fetch info for all games from MobyGames")
        fetchAct.triggered.connect(self.fetchInfo)

        act = {"add": addAct, "del": delAct, "det": detAct, "export": expAct,
               "import": impAct, "steam": stmAct, "owned": ownAct,
               "delnotowned": delNotOwned, "about": aboutAct, "exit": exitAct,
               "info": infoAct, "fetch": fetchAct}

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

        if 0 < currentTab < 4:
            cmenu.addAction(self.buttonActions("det"))
            cmenu.addAction(self.buttonActions("del"))
            cmenu.addAction(self.buttonActions("info"))
            cmenu.exec_(self.mapToGlobal(event.pos()))

        self.search()

    def info(self):
        currentTab = self.tab.currentIndex()
        indexes = self.tableViewList[currentTab-1].selectedIndexes()
        rows = [index.row() for index in indexes]
        for _ in rows:
            self.tableViewList[currentTab-1].rowInfo()

    def search(self):
        """Filters table contents based on user input"""

        currentTab = self.tab.currentIndex()

        if 0 < currentTab < 4:
            searchText = self.searchBox.text()
            self.searchLabel.setVisible(True)
            self.searchBox.setVisible(True)
            self.filterBtn.setVisible(True)
            self.searchBtn.setVisible(True)
            self.filterDock.setItemType(currentTab)
            itemCount = self.tableViewList[currentTab - 1].filterTable(searchText, self.filterDock.getSelections())

            if searchText != "" or len(self.filterDock.getSelections()) > 0:
                self.statusBar().showMessage("Found {} {}.".format(itemCount,
                                                                   self.tableViewList[currentTab-1].model.tableName()))
            else:
                self.updateStatusbar()
        else:
            self.searchLabel.setVisible(False)
            self.searchBox.setVisible(False)
            self.filterBtn.setVisible(False)
            self.searchBtn.setVisible(False)
            if self.filterDock.isVisible():
                self.filterDock.toggleVisibility()

    def toggleOwnedFilter(self):
        for table in self.tableViewList:
            table.setHideNotOwned(False) if table.hideNotOwned\
                else table.setHideNotOwned(True)
        currentTab = self.tab.currentIndex()
        if 0 < currentTab < 4:
            self.tableViewList[currentTab-1].filterTable(self.searchBox.text(), self.filterDock.getSelections())
        self.search()

    def updateStatusbar(self):
        currentTab = self.tab.currentIndex()
        itemType = ["games", "consoles", "accessories"]

        if currentTab == 0:
            self.statusBar().showMessage("")
        elif 0 < currentTab < 4:
            numItems = self.tableViewList[currentTab-1].ownedCount
            if self.tableViewList[currentTab-1].hideNotOwned:
                self.statusBar().showMessage(f"{numItems} {itemType[currentTab-1]} in collection.")
            else:
                self.statusBar().showMessage("Showing {} {} ({} {} in collection).".format(
                    self.tableViewList[currentTab-1].allCount,
                    itemType[currentTab-1],
                    numItems,
                    itemType[currentTab-1]))
        elif currentTab == 4:
            platforms = self.randomizer.consoleList.selectedItems()
            genres = self.randomizer.genreList.selectedItems()
            self.statusBar().showMessage("Select platforms or genre to randomize from.")
            if len(platforms) > 0 or len(genres) > 0:
                self.statusBar().showMessage(f"Selecting from {self.randomizer.gameCount()} games.")
            return
