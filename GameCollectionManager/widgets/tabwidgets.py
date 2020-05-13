from collections import OrderedDict
from random import randint

from PySide2.QtCore import Qt, Signal, QModelIndex
from PySide2.QtGui import QFont
from PySide2.QtSql import QSqlTableModel, QSqlQuery
from PySide2.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, \
    QPushButton, QLabel, QListWidget, QAbstractItemView, QTableView
from widgets.models import TableModel


class Table(QTableView):

    resized = Signal()
    fetched = Signal()

    def __init__(self, tableName: str, db):
        super(Table, self).__init__()

        self.resized.connect(self.resizeRowsToContents)
        self.fetched.connect(self.resizeRowsToContents)

        assert tableName in ("games", "consoles", "accessories")

        self._db = db
        self._hideNotOwned = True
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
            self.model.setHeaderData(9, Qt.Horizontal, "Comment")
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
                    query.exec_("INSERT INTO {} "
                                "(ID, Platform, Name, Region, Code, Game, Box, Manual, Year, Comment) "
                                "VALUES "
                                "({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        table, itemID, data["Platform"], data["Name"], data["Region"], data["Code"],
                        data["Game"], data["Box"], data["Manual"], data["Year"], data["Comment"])
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
                            "(ID, Platform, Name, Region, Code, Game, Box, Manual, Year, Comment) "
                            "VALUES "
                            "({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                    table, itemID, newData["Platform"], newData["Name"], newData["Region"], newData["Code"],
                    newData["Game"], newData["Box"], newData["Manual"], newData["Year"], newData["Comment"])
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
            if self._hideNotOwned:
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
            if self._hideNotOwned:
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
            if self._hideNotOwned:
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
        query.exec_("SELECT Platform, Name, Region "
                    f"FROM {self._table} WHERE {self._itemType}='Yes' OR Box='Yes' OR Manual='Yes'")
        while query.next():
            items.append(dict(Platform=query.value(0), Name=query.value(1), Region=query.value(2)))

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

    def rowInfo(self, row: int):
        table = self._table
        query = QSqlQuery()
        length = 11 if table == "consoles" else 10

        query.exec_(f"SELECT * FROM {table} WHERE ID={row}")
        query.first()

        for i in range(length):
            print(query.value(i))

    def setHideNotOwned(self, on: bool):
        self._hideNotOwned = on

        """if self.hideNotOwned:
            names = []
            table = self.table
            item = "Game" if table == "games" else\
                "Console" if table == "consoles" else\
                "Accessory"
            query = QSqlQuery()
            query.exec_("SELECT Name FROM {} WHERE {}='No' AND Box='No' AND Manual='No'".format(
                table, item
            ))
            while query.next():
                names.append(query.value(0))

            while self.model.canFetchMore():
                self.model.fetchMore()

            for name in names:
                for row in range(self.model.rowCount()):
                    text = self.indexAt(QPoint(2, row))
                    game = self.indexAt(QPoint(5, row))
                    box = self.indexAt(QPoint(6, row))
                    manual = self.indexAt(QPoint(7, row))
                    print(row, name, text.data(), game.data(), box.data(), manual.data())  # ???

                    if text.data() == name and game.data() == 'No'\
                            and box.data() == 'No' and manual.data() == 'No':
                        self.setRowHidden(row, True)"""

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

        self.consoleList = QListWidget()
        self._consoleItems = set()
        for row in gamesData:
            self._consoleItems.add(row["Platform"])
        self.consoleList.addItems(sorted(self._consoleItems, key=str.lower))
        self.consoleList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.consoleList.setMaximumWidth(350)
        self.consoleList.itemClicked.connect(self._updateGameCount)

        self.btnAll = QPushButton("Select All")
        self.btnAll.setMaximumSize(self.btnAll.sizeHint())
        self.btnAll.clicked.connect(self.consoleList.selectAll)
        self.btnAll.clicked.connect(self._updateGameCount)
        self.btnNone = QPushButton("Select None")
        self.btnNone.setMaximumSize(self.btnNone.sizeHint())
        self.btnNone.clicked.connect(self.consoleList.clearSelection)
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

        self._hbox = QHBoxLayout()
        self._vbox = QVBoxLayout()
        self._grid = QGridLayout()
        self._hbox.addWidget(self.btnAll, 0)
        self._hbox.addWidget(self.btnNone, 0)
        self._hbox.addWidget(self._btnRnd, 0)
        self._vbox.addStretch(3)
        self._vbox.addWidget(self._lblPlay, 1)
        self._vbox.addWidget(self._lblTitle, 1)
        self._vbox.addStretch(3)
        self._grid.setMargin(0)
        self._grid.setSpacing(0)
        self._grid.addWidget(self.consoleList, 0, 0)
        self._grid.addLayout(self._hbox, 1, 0)
        self._grid.addLayout(self._vbox, 0, 1, 1, -1)

        self.widget = QWidget()
        self.widget.setLayout(self._grid)

    def _getSelectedPlatforms(self) -> list:
        return [x.text() for x in self.consoleList.selectedItems()]

    def _randomize(self):
        platforms = self._getSelectedPlatforms()
        games = []

        if len(platforms) > 0:
            for row in self._gamesData:
                if row["Platform"] in platforms:
                    games.append(row)

            choice = randint(0, len(games) - 1)
            self._lblPlay.setText("You will play:")
            self._lblTitle.setText(f"{games[choice]['Name']}" if len(platforms) == 1 else
                                   f"{games[choice]['Name']} [{games[choice]['Platform']}]")
        else:
            self._lblPlay.setText("")
            self._lblTitle.setText("Select at least one console...")

    def _updateGameCount(self):
        platforms = self._getSelectedPlatforms()
        self._gameCount = 0

        if len(platforms) > 0:
            for row in self._gamesData:
                if row["Platform"] in platforms:
                    self._gameCount += 1

    def gameCount(self) -> int:
        return self._gameCount

    def updateData(self, gamesData: list):
        self._gamesData.clear()
        self._consoleItems.clear()
        self.consoleList.clear()

        self._gamesData = gamesData
        for row in self._gamesData:
            self._consoleItems.add(row["Platform"])
        self.consoleList.addItems(sorted(self._consoleItems, key=str.lower))
