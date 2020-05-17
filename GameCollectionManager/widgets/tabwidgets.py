from collections import OrderedDict
from random import randint

from PySide2.QtCore import Qt, Signal, QModelIndex, QItemSelectionModel
from PySide2.QtGui import QFont, QKeyEvent, QMouseEvent
from PySide2.QtSql import QSqlTableModel, QSqlQuery
from PySide2.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, \
    QPushButton, QLabel, QListWidget, QAbstractItemView, QTableView
from widgets.models import TableModel
from utilities.fetchinfo import getMobyInfo, printInfo


class Table(QTableView):

    resized = Signal()
    fetched = Signal()
    doubleClick = Signal(dict)

    def __init__(self, tableName: str, db):
        super(Table, self).__init__()

        self.resized.connect(self.resizeRowsToContents)
        self.fetched.connect(self.resizeRowsToContents)

        assert tableName in ("games", "consoles", "accessories")

        self._db = db
        self.hideNotOwned = True
        self._table = tableName
        self._itemType = "Game" if self._table == "games"\
            else "Console" if self._table == "consoles"\
            else "Accessory"

        self.model = TableModel(self, self._db)
        self.model.setTable(tableName)
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Platform")
        self.model.setHeaderData(2, Qt.Horizontal, "Name")
        self.model.setHeaderData(3, Qt.Horizontal, "Region")
        if self._table == "games":
            self.model.setHeaderData(4, Qt.Horizontal, "Code")
            self.model.setHeaderData(5, Qt.Horizontal, "Game")
            #self.setItemDelegateForColumn(5, CheckboxDelegate("Game", parent=self))
            self.model.setHeaderData(6, Qt.Horizontal, "Box")
            #self.setItemDelegateForColumn(6, CheckboxDelegate("Box", parent=self))
            self.model.setHeaderData(7, Qt.Horizontal, "Manual")
            #self.setItemDelegateForColumn(7, CheckboxDelegate("Manual", parent=self))
            self.model.setHeaderData(8, Qt.Horizontal, "Year")
            self.model.setHeaderData(9, Qt.Horizontal, "Genre")
            self.model.setHeaderData(10, Qt.Horizontal, "Comment")
            self.model.setHeaderData(11, Qt.Horizontal, "Publisher")
            self.model.setHeaderData(12, Qt.Horizontal, "Developer")
            self.model.setHeaderData(13, Qt.Horizontal, "Platforms")
            # Hide the publisher, developer, and platforms columns
        elif self._table == "consoles":
            self.model.setHeaderData(4, Qt.Horizontal, "Country")
            self.model.setHeaderData(5, Qt.Horizontal, "Serial number")
            self.model.setHeaderData(6, Qt.Horizontal, "Console")
            #self.setItemDelegateForColumn(6, CheckboxDelegate("Console", parent=self))
            self.model.setHeaderData(7, Qt.Horizontal, "Box")
            #self.setItemDelegateForColumn(7, CheckboxDelegate("Box", parent=self))
            self.model.setHeaderData(8, Qt.Horizontal, "Manual")
            #self.setItemDelegateForColumn(8, CheckboxDelegate("Manual", parent=self))
            self.model.setHeaderData(9, Qt.Horizontal, "Year")
            self.model.setHeaderData(10, Qt.Horizontal, "Comment")
        elif self._table == "accessories":
            self.model.setHeaderData(4, Qt.Horizontal, "Country")
            self.model.setHeaderData(5, Qt.Horizontal, "Accessory")
            #self.setItemDelegateForColumn(5, CheckboxDelegate("Accessory", parent=self))
            self.model.setHeaderData(6, Qt.Horizontal, "Box")
            #self.setItemDelegateForColumn(6, CheckboxDelegate("Box", parent=self))
            self.model.setHeaderData(7, Qt.Horizontal, "Manual")
            #self.setItemDelegateForColumn(7, CheckboxDelegate("Manual", parent=self))
            self.model.setHeaderData(8, Qt.Horizontal, "Year")
            self.model.setHeaderData(9, Qt.Horizontal, "Comment")

        self.setModel(self.model)

        # Column widths
        self.horizontalHeader().setStretchLastSection(True)
        for column in range(self.model.columnCount()):
            if self.model.headerData(column, Qt.Horizontal) == "Platform":
                self.setColumnWidth(column, 100)
            elif self.model.headerData(column, Qt.Horizontal) == "Name":
                self.setColumnWidth(column, 300)
            elif self.model.headerData(column, Qt.Horizontal) in ("Region", "Country"):
                self.setColumnWidth(column, 85)
            elif self.model.headerData(column, Qt.Horizontal) in ("Code", "Serial number"):
                self.setColumnWidth(column, 140)
            elif self.model.headerData(column, Qt.Horizontal) == "Year":
                self.setColumnWidth(column, 40)
            elif self.model.headerData(column, Qt.Horizontal) in ("Game", "Console", "Accessory", "Box", "Manual"):
                self.setColumnWidth(column, 70)

        self.verticalHeader().setVisible(False)  # Don't show row headers
        self.setColumnHidden(0, True)  # Don't show ID field
        # Hide the Publisher, Developer, and Platforms columns since it's for internal use
        self.setColumnHidden(11, True)
        self.setColumnHidden(12, True)
        self.setColumnHidden(13, True)
        self.setAlternatingRowColors(False)
        self.setShowGrid(True)
        self.resizeRowsToContents()

    def addData(self, newData):
        """
        Adds data to the SQL database
        :param newData: (dictionary or list of dictionaries) The data to be added
        """

        table = self._table
        itemID = 0 if self.model.rowCount() == 0 else -1
        query = QSqlQuery()

        if isinstance(newData, list):
            if itemID != 0:
                query.exec_(f"SELECT COUNT(*) FROM {table}")
                query.first()
                itemID = query.value(0)

            for data in newData:
                if table == "games":
                    # SQLite3 doesn't support batch execution so just execute each statement is sequence.
                    query.exec_("INSERT INTO {} "
                                "(ID, Platform, Name, Region, Code, Game, Box, Manual, Year, Genre, Comment, "
                                "Publisher, Developer, Platforms) "
                                "VALUES "
                                "({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        table, itemID, data["Platform"], data["Name"], data["Region"], data["Code"],
                        data["Game"], data["Box"], data["Manual"], data["Year"], data["Genre"], data["Comment"],
                        data["Publisher"], data["Developer"], data["Platforms"])
                    )
                elif table == "consoles":
                    query.exec_("INSERT INTO {} "
                                "(ID, Platform, Name, Region, Country, `Serial number`, Console, Box, Manual, "
                                "Year, Comment) "
                                "VALUES "
                                "({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        table, itemID, data["Platform"], data["Name"], data["Region"], data["Country"],
                        data["Serial number"], data["Console"], data["Box"], data["Manual"], data["Year"],
                        data["Comment"])
                    )
                elif table == "accessories":
                    query.exec_("INSERT INTO {} "
                                "(ID, Platform, Name, Region, Country, Accessory, Box, Manual, Year, Comment) "
                                "VALUES "
                                "({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        table, itemID, data["Platform"], data["Name"], data["Region"], data["Country"],
                        data["Accessory"], data["Box"], data["Manual"], data["Year"], data["Comment"])
                    )
                itemID += 1

        elif isinstance(newData, OrderedDict) or isinstance(newData, dict):
            if itemID != 0:
                query.exec_(f"SELECT COUNT(*) FROM {table}")
                query.first()
                itemID = query.value(0)

            if table == "games":
                query.exec_("INSERT INTO {} "
                            "(ID, Platform, Name, Region, Code, Game, Box, Manual, Year, Genre, Comment, "
                            "Publisher, Developer, Platforms) "
                            "VALUES "
                            "({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        table, itemID, newData["Platform"], newData["Name"], newData["Region"], newData["Code"],
                        newData["Game"], newData["Box"], newData["Manual"], newData["Year"], newData["Genre"], newData["Comment"],
                        newData["Publisher"], newData["Developer"], newData["Platforms"])
                )
            elif table == "consoles":
                query.exec_("INSERT INTO {} "
                            "(ID, Platform, Name, Region, Country, `Serial number`, Console, Box, Manual, "
                            "Year, Comment) "
                            "VALUES "
                            "({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                    table, itemID, newData["Platform"], newData["Name"], newData["Region"], newData["Country"],
                    newData["Serial number"], newData["Console"], newData["Box"], newData["Manual"], newData["Year"],
                    newData["Comment"])
                )
            elif table == "accessories":
                query.exec_("INSERT INTO {} "
                            "(ID, Platform, Name, Region, Country, Accessory, Box, Manual, Year, Comment) "
                            "VALUES "
                            "({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                    table, itemID, newData["Platform"], newData["Name"], newData["Region"], newData["Country"],
                    newData["Accessory"], newData["Box"], newData["Manual"], newData["Year"], newData["Comment"])
                )

        self.filterTable("", dict())

    def deleteData(self, rows: list):
        """
        Deletes rows from SQL database
        :param rows: Rows to delete
        """

        for row in rows:
            self.model.removeRows(row, 1, parent=QModelIndex())
        self.model.select()
        self.resizeRowsToContents()

    def deleteNotOwned(self):
        rows = []
        query = QSqlQuery()
        query.exec_(f"SELECT ID FROM {self._table} WHERE {self._itemType}='No' AND Box='No' AND Manual='No'")
        while query.next():
            rows.append(query.value(0))

        for row in rows:
            query.exec_(f"DELETE FROM {self._table} WHERE ID={row}")
        self.model.select()
        self.resizeRowsToContents()

    def filterTable(self, filterText: str, selections: dict):
        """
        Filters the table based on search strings
        :param filterText: The text to filter
        :param selections: Possible selected items from advanced search options
        """

        # Reset filtering to default if no search filters
        if filterText == "" and len(selections) == 0:
            if self.hideNotOwned:
                self.model.setFilter(f"{self._itemType}='Yes' OR Box='Yes' OR Manual='Yes' "
                                     "ORDER BY Platform ASC, Name ASC")
            else:
                self.model.setFilter("1=1 ORDER BY Platform ASC, Name ASC")
            self.resizeRowsToContents()
            return

        # Filter based on advanced search options
        elif len(selections) > 0:
            f = f"(Name LIKE '%{filterText}%' " \
                f"OR Year LIKE '%{filterText}%' " \
                f"OR Comment LIKE '%{filterText}%') "
            if self.hideNotOwned:
                f += f"AND ({self._itemType}='Yes' OR Box='Yes' OR Manual='Yes') "
            for selection in selections:
                items = list(selections[selection])
                f += f"AND ({selection} = '{items[0]}' "
                if len(items) > 1:
                    for item in items[1:]:
                        f += f"OR {selection} = '{item}' "
                f += ") "
        else:  # Regular, simple, filter. It just seaches almost every column
            f = f"(Platform LIKE '%{filterText}%' " \
                f"OR Name LIKE '%{filterText}%' " \
                f"OR Region LIKE '%{filterText}%' " \
                f"OR Comment LIKE '%{filterText}%' " \
                f"OR Year LIKE '%{filterText}%' "
            if self._table == "games":
                f += f"OR Code LIKE '%{filterText}%') "
            elif self._table == "consoles":
                f += f"OR Country LIKE '%{filterText}%' " \
                     f"OR `Serial number` LIKE '%{filterText}%') "
            elif self._table == "accessories":
                f += f"OR Country LIKE '%{filterText}%') "
            if self.hideNotOwned:
                f += f"AND ({self._itemType}='Yes' OR Box='Yes' OR Manual='Yes') "

        f += "ORDER BY Platform ASC, Name ASC"

        self.model.setFilter(f)
        self.resizeRowsToContents()

    def itemsInPlatform(self, platform: str) -> int:
        """
        Counts how many items are in a platform
        :param platform: Platform to count items for
        :return: (int) Item count
        """

        count = 0

        query = QSqlQuery()
        query.exec_(f"SELECT Name FROM {self._table} WHERE Platform='{platform}'"
                    f"AND ({self._itemType}='Yes' OR Box='Yes' OR Manual='Yes')")
        while query.next():
            count += 1

        return count

    def keyPressEvent(self, event: QKeyEvent):
        # Custom handling for enter key to start editing
        if event.key() == Qt.Key_Return:
            nextRow = self.currentIndex().row() + 1
            if nextRow > self.model.rowCount(self.currentIndex()):
                # Can't go further down
                nextRow -= 1
            if self.state() == QAbstractItemView.EditingState:
                nextIndex = self.model.index(nextRow, self.currentIndex().column())
                self.setCurrentIndex(nextIndex)
                self.selectionModel().select(nextIndex, QItemSelectionModel.ClearAndSelect)
            else:
                # If we're not editing, start editing
                self.edit(self.currentIndex())
        else:
            super(Table, self).keyPressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        # Custom handling for double clicking so we open the side panel
        if event.button() == Qt.LeftButton:
            self.rowData()
        else:
            super(Table, self).mouseDoubleClickEvent(event)

    def ownedCount(self) -> int:
        """
        Counts how many items in the table that are owned. An owned item is one that
        has either the item itself, the box, or the manual.
        :return: (int) Item count
        """

        count = 0

        query = QSqlQuery()
        query.exec_(f"SELECT Name FROM {self._table} WHERE {self._itemType}='Yes' OR Box='Yes' OR Manual='Yes'")
        while query.next():
            count += 1

        return count

    def ownedItems(self) -> list:
        """
        Fetches all items in the table that are owned. An owned item is one that
        has either the item itself, the box, or the manual.
        :return: (list) List of items
        """

        items = []

        query = QSqlQuery()
        query.exec_("SELECT Platform, Name, Region, Genre "
                    f"FROM {self._table} WHERE {self._itemType}='Yes' OR Box='Yes' OR Manual='Yes'")
        while query.next():
            items.append(dict(Platform=query.value(0), Name=query.value(1), Region=query.value(2), Genre=query.value(3)))

        return items

    def platforms(self) -> set:
        """
        Fetches the platforms that are currently in the table.
        :return: (set) Platforms in table
        """

        platforms = set()

        query = QSqlQuery()
        query.exec_(f"SELECT Platform FROM {self._table}")
        while query.next():
            platforms.add(query.value(0))

        return platforms

    def resizeEvent(self, event):
        """
        Currently doesn't seem to trigger when pressing window manager minimize/maximize button
        """

        self.resized.emit()
        return super().resizeEvent(event)

    def rowCountChanged(self, oldCount: int, newCount: int):
        self.fetched.emit()
        return super().rowCountChanged(oldCount, newCount)

    def rowData(self):
        rowData = {}
        gamesColumns = ["Id", "Platform", "Name", "Region", "Code", "Game", "Box", "Manual", "Year", "Genre",
                        "Comment", "Publisher", "Developer", "Platforms"]
        consoleColumns = ["Id", "Platform", "Name", "Region", "Country", "Serial number", "Console", "Box",
                          "Manual", "Year", "Comment"]
        accessoriesColumns = ["Id", "Platform", "Name", "Region", "Country", "Accessory", "Box", "Manual",
                              "Year", "Comment"]

        id = self.model.index(self.currentIndex().row(), 0).data()
        query = QSqlQuery()
        query.exec_(f"SELECT * FROM {self._table} WHERE Id={id}")
        query.first()
        if self._table == "games":
            for i in range(1, len(gamesColumns)):
                rowData[gamesColumns[i]] = query.value(i)

            self.doubleClick.emit(rowData)

    def rowInfo(self, row: int):
        table = self._table
        query = QSqlQuery()
        length = 10 if table == "accessories" else 11

        query.exec_(f"SELECT * FROM {table} WHERE ID={row}")
        query.first()

        title = ""
        platform = ""
        columns = {"games": ["Id", "Platform", "Name", "Region", "Code", "Game", "Box", "Manual", "Year", "Genre", "Comment"],
                   "consoles": ["Id", "Platform", "Name", "Region", "Country", "Serial number", "Console", "Box", "Manual", "Year", "Comment"],
                   "accessories": ["Id", "Platform", "Name", "Region", "Country", "Accessory", "Box", "Manual", "Year", "Comment"]}

        for i in range(length):
            if table == "games":
                if i == 1:
                    platform = query.value(i)
                if i == 2:
                    title = query.value(i)
            col = columns[table][i]
            print(col, end=":\t" if len(col) > 6 else ":\t\t\t" if len(col) < 3 else ":\t\t")
            print(query.value(i))

        print()

        if table == "games":
            info = getMobyInfo(title, platform)
            printInfo(info)

    def setHideNotOwned(self, on: bool):
        self.hideNotOwned = on

    def test(self):
        pass


class Randomizer(QWidget):
    """A game randomizer for selecting a random game to play
       from the user's collection. User can select which
       platforms to choose from.
       gamesData: Raw table data in list of orderedDicts"""

    def __init__(self, gamesData: list):
        super(Randomizer, self).__init__()

        self._gamesData = gamesData
        self._gameCount = 0

        self._consoleItems = set()
        self._genreItems = set()
        for row in gamesData:
            self._consoleItems.add(row["Platform"])
            if row["Genre"] != "":
                self._genreItems.add(row["Genre"])

        self.consoleLabel = QLabel("Platforms")
        self.consoleList = QListWidget()
        self.consoleList.addItems(sorted(self._consoleItems, key=str.lower))
        self.consoleList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.consoleList.setMaximumWidth(350)
        self.consoleList.itemClicked.connect(self._updateGameCount)

        self.genreLabel = QLabel("Genres")
        self.genreList = QListWidget()
        self.genreList.addItems(sorted(self._genreItems, key=str.lower))
        self.genreList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.genreList.setMaximumWidth(350)
        self.genreList.itemClicked.connect(self._updateGameCount)

        self.btnAll = QPushButton("Select All")
        self.btnAll.setMaximumSize(self.btnAll.sizeHint())
        self.btnAll.clicked.connect(self.consoleList.selectAll)
        self.btnAll.clicked.connect(self.genreList.selectAll)
        self.btnAll.clicked.connect(self._updateGameCount)
        self.btnNone = QPushButton("Select None")
        self.btnNone.setMaximumSize(self.btnNone.sizeHint())
        self.btnNone.clicked.connect(self.consoleList.clearSelection)
        self.btnNone.clicked.connect(self.genreList.clearSelection)
        self.btnNone.clicked.connect(self._updateGameCount)
        self._btnRnd = QPushButton("Randomize")
        self._btnRnd.setMaximumSize(self._btnRnd.sizeHint())
        self._btnRnd.clicked.connect(self._randomize)

        self._lblFont = QFont()
        self._lblFont.setPointSize(14)
        self._lblFont.setBold(True)
        self._lblPlay = QLabel()
        self._lblPlay.setAlignment(Qt.AlignCenter)
        self._lblPlay.setFont(self._lblFont)
        self._lblTitle = QLabel()
        self._lblTitle.setAlignment(Qt.AlignCenter)
        self._lblTitle.setFont(self._lblFont)
        self._lblTitle.setWordWrap(True)

        self._hboxButtons = QHBoxLayout()
        self._vboxLists = QVBoxLayout()
        self._vboxConsoles = QVBoxLayout()
        self._vboxGenres = QVBoxLayout()
        self._vboxResult = QVBoxLayout()
        self._grid = QGridLayout()
        self._hboxButtons.addWidget(self.btnAll, 0)
        self._hboxButtons.addWidget(self.btnNone, 0)
        self._hboxButtons.addWidget(self._btnRnd, 0)
        self._vboxConsoles.addWidget(self.consoleLabel, 0)
        self._vboxConsoles.addWidget(self.consoleList, 1)
        self._vboxGenres.addWidget(self.genreLabel, 0)
        self._vboxGenres.addWidget(self.genreList, 1)
        self._vboxLists.addSpacing(10)
        self._vboxLists.addLayout(self._vboxConsoles, 1)
        self._vboxLists.addSpacing(10)
        self._vboxLists.addLayout(self._vboxGenres, 1)
        self._vboxResult.addStretch(3)
        self._vboxResult.addWidget(self._lblPlay, 1)
        self._vboxResult.addWidget(self._lblTitle, 1)
        self._vboxResult.addStretch(3)
        self._grid.setMargin(0)
        self._grid.setSpacing(0)
        self._grid.addLayout(self._vboxLists, 0, 0)
        self._grid.addLayout(self._hboxButtons, 1, 0)
        self._grid.addLayout(self._vboxResult, 0, 1, 1, -1)

        self.widget = QWidget()
        self.widget.setLayout(self._grid)

    def _getSelectedItems(self) -> tuple:
        return [x.text() for x in self.consoleList.selectedItems()], [x.text() for x in self.genreList.selectedItems()]

    def _randomize(self):
        platforms, genres = self._getSelectedItems()
        games = []

        if len(platforms) > 0 or len(genres) > 0:
            for row in self._gamesData:
                if len(platforms) > 0 and len(genres) > 0:
                    if row["Platform"] in platforms and row["Genre"] in genres:
                        games.append(row)
                elif len(platforms) > 0 and len(genres) == 0:
                    if row["Platform"] in platforms:
                        games.append(row)
                elif len(platforms) == 0 and len(genres) > 0:
                    if row["Genre"] in genres:
                        games.append(row)

            choice = randint(0, len(games) - 1)
            self._lblPlay.setText("You will play:")
            self._lblTitle.setText(f"{games[choice]['Name']}" if len(platforms) == 1 else
                                   f"{games[choice]['Name']} [{games[choice]['Platform']}]")
        else:
            self._lblPlay.setText("")
            self._lblTitle.setText("Select at least one console or genre...")

    def _updateGameCount(self):
        platforms, genres = self._getSelectedItems()
        self._gameCount = 0

        if len(platforms) > 0 or len(genres) > 0:
            for row in self._gamesData:
                if len(platforms) > 0 and len(genres) > 0:
                    if row["Platform"] in platforms and row["Genre"] in genres:
                        self._gameCount += 1
                elif len(platforms) > 0 and len(genres) == 0:
                    if row["Platform"] in platforms:
                        self._gameCount += 1
                elif len(platforms) == 0 and len(genres) > 0:
                    if row["Genre"] in genres:
                        self._gameCount += 1

    def gameCount(self) -> int:
        return self._gameCount

    def updateData(self, gamesData: list):
        self._gamesData.clear()
        self._consoleItems.clear()
        self.consoleList.clear()
        self._genreItems.clear()
        self.genreList.clear()

        self._gamesData = gamesData
        for row in self._gamesData:
            self._consoleItems.add(row["Platform"])
            self._genreItems.add(row["Genre"])
        self.consoleList.addItems(sorted(self._consoleItems, key=str.lower))
        self.genreList.addItems(sorted(self._genreItems, key=str.lower))
