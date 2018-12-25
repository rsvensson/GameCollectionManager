from PySide2.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,\
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,\
    QListWidget, QAbstractItemView, QTableView, QMessageBox
from PySide2.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery, QSqlRecord
from PySide2.QtGui import QColor, QFont
from PySide2.QtCore import Qt, Signal
from collections import OrderedDict
from random import randint

from widgets.models import TableModel
from widgets.delegates import CheckboxDelegate


class Randomizer(QWidget):
    """A game randomizer for selecting a random game to play
       from the user's collection. User can select which
       platforms to choose from.
       gamesData: Raw table data in list of orderedDicts"""

    def __init__(self, gamesData):
        super().__init__()

        self.gamesData = gamesData

        self.gameCount = 0

        self.consoleList = QListWidget()
        self.consoleItems = set()
        for row in gamesData:
            for col in row:
                if col == "Platform":
                    self.consoleItems.add(row[col])
        self.consoleList.addItems(sorted(self.consoleItems))
        self.consoleList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.consoleList.setMaximumWidth(350)
        self.consoleList.itemClicked.connect(self._updateGameCount)

        self.btnAll = QPushButton()
        self.btnAll.setText("Select All")
        self.btnAll.setMaximumSize(self.btnAll.sizeHint())
        self.btnAll.clicked.connect(self.consoleList.selectAll)
        self.btnAll.clicked.connect(self._updateGameCount)
        self.btnNone = QPushButton()
        self.btnNone.setText("Select None")
        self.btnNone.setMaximumSize(self.btnNone.sizeHint())
        self.btnNone.clicked.connect(self.consoleList.clearSelection)
        self.btnNone.clicked.connect(self._updateGameCount)
        self.btnRnd = QPushButton()
        self.btnRnd.setText("Randomize")
        self.btnRnd.setMaximumSize(self.btnRnd.sizeHint())
        self.btnRnd.clicked.connect(self._randomize)

        self.lblFont = QFont()
        self.lblFont.setPointSize(14)
        self.lblFont.setBold(True)
        self.lblPlay = QLabel()
        self.lblPlay.setAlignment(Qt.AlignCenter)
        self.lblPlay.setFont(self.lblFont)
        self.lblTitle = QLabel()
        self.lblTitle.setAlignment(Qt.AlignCenter)
        self.lblTitle.setFont(self.lblFont)
        self.lblTitle.setWordWrap(True)

        self.Grid = QGridLayout()
        self.Grid.setMargin(0)
        self.Grid.setSpacing(0)
        self.HBox = QHBoxLayout()
        self.VBox = QVBoxLayout()
        self.HBox.addWidget(self.btnAll, 0)
        self.HBox.addWidget(self.btnNone, 0)
        self.HBox.addWidget(self.btnRnd, 0)
        self.VBox.addStretch(3)
        self.VBox.addWidget(self.lblPlay, 1)
        self.VBox.addWidget(self.lblTitle, 1)
        self.VBox.addStretch(3)
        self.Grid.addWidget(self.consoleList, 0, 0)
        self.Grid.addLayout(self.HBox, 1, 0)
        self.Grid.addLayout(self.VBox, 0, 1, 1, -1)

        self.layout = QWidget()
        self.layout.setLayout(self.Grid)

    def _getSelectedPlatforms(self):
        return [x.text() for x in self.consoleList.selectedItems()]

    def _randomize(self):
        platforms = self._getSelectedPlatforms()
        games = []

        if len(platforms) > 0:
            for row in self.gamesData:
                for col in row:
                    if col == "Platform" and row[col] in platforms:
                        games.append(row)

            choice = randint(0, len(games) - 1)
            self.lblPlay.setText("You will play:")
            self.lblTitle.setText("{}".format(games[choice]["Name"]) if len(platforms) == 1 else
                                  "{} [{}]".format(games[choice]["Name"], games[choice]["Platform"]))
        else:
            self.lblPlay.setText("")
            self.lblTitle.setText("Select at least one console...")

    def _updateGameCount(self):
        platforms = self._getSelectedPlatforms()
        self.gameCount = 0

        if len(platforms) > 0:
            for row in self.gamesData:
                for col in row:
                    if col == "Platform" and row[col] in platforms:
                        self.gameCount += 1

    def getGameCount(self):
        return self.gameCount


class Table(QTableWidget):
    """Creates a QTableWidget, populates it and controls its data"""

    # Signal to send when table has been edited
    updated = Signal()

    # Signal to detect window resizing
    resized = Signal()

    def __init__(self, tableDB):
        """
        tableDB: A 'Database' (csv/tsv) object
        """
        super().__init__()

        self._tableDB = tableDB
        self._tableData = self._tableDB.connect()  # _tableData is a list of orderedDict

        # List of dicts holding data about table items. Gets appended to in _populateTable.
        # Keys: "Name" (str), "Row" (int), "In collection" (bool).
        self._items = []

        self._hideNotOwned = False
        if self._hideNotOwned:
            self.searchTable("")
        self._isUpdating = False  # So _onEdit doesn't enter an endless loop
        self._populateTable()

        self.cellChanged.connect(self._onEdit)
        self.resized.connect(self._resize)

    def _onEdit(self, row, column):
        """Method for handling editing of cells
           row, column: Cell row and column of edited cell"""

        if not self._isUpdating:  # We need this check or we will enter an endless loop
            editedRow = []        # when we update the table rows.
            keys = self._tableData[0].keys()
            rowToDelete = 0

            for col, key in enumerate(keys):
                if key == "Name":
                    # Get the actual row in database to delete
                    for itemRow in range(len(self._items)):
                        if self.item(row, col).text() in self._items[itemRow]["Name"]:
                            rowToDelete = self._items[itemRow]["Row"]
                            break

                if key in ["Game", "Console", "Accessory", "Box", "Manual"]:
                    # Convert checkboxes to text
                    if self.item(row, col).data(Qt.CheckStateRole) == Qt.Checked:
                        editedRow.append("Yes")
                        continue
                    elif self.item(row, col).data(Qt.CheckStateRole) == Qt.Unchecked:
                        editedRow.append("No")
                        continue

                editedRow.append(self.item(row, col).text())

            newRow = OrderedDict()
            for i, key in enumerate(keys):
                newRow[key] = editedRow[i]

            del self._tableData[rowToDelete]
            self.addData(newRow)

    def _populateTable(self):
        """Populates and formats table data"""

        if len(self._tableData) < 1:  # Handles empty tables
            self.setColumnCount(len(self._tableData))
            self.setHorizontalHeaderLabels([h.capitalize() for h in self._tableData])
        else:
            self.setColumnCount(len(self._tableData[0]))
            self.setHorizontalHeaderLabels([h.capitalize() for h in self._tableData[0]])

        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.setSortingEnabled(False)
        bold = QFont()
        bold.setBold(True)

        self._items.clear()  # Start from the beginning again

        for i, row in enumerate(self._tableData):
            self.insertRow(self.rowCount())
            self._items.append(dict())

            for j, col in enumerate(row):
                item = QTableWidgetItem()
                item.setText(row[col])

                if col == "Platform":
                    self.setColumnWidth(j, 100)
                    self._items[i]["Platform"] = row[col]
                elif col == "Name":
                    self.setColumnWidth(j, 300)
                    self._items[i]["Name"] = row[col]
                    self._items[i]["Row"] = i  # Saves item's place in db file!
                elif col == "Region":
                    self.setColumnWidth(j, 85)
                    item.setTextAlignment(Qt.AlignCenter)
                    if "NTSC" in row[col]:
                        item.setFont(bold)
                        item.setForeground(QColor(0, 255, 255))
                    if row[col] in ["NTSC (JP)", "Japan"]:
                        item.setFont(bold)
                        item.setForeground(QColor(255, 0, 0))
                    if row[col] in ["NTSC (NA)", "North America"]:
                        item.setFont(bold)
                        item.setForeground(QColor(0, 0, 255))
                    if row[col] in ["PAL", "Europe"]:
                        item.setFont(bold)
                        item.setForeground(QColor(255, 255, 0))
                elif col == "Country":
                    self.setColumnWidth(j, 75)
                    item.setTextAlignment(Qt.AlignCenter)
                    if row[col] == "JPN":
                        item.setFont(bold)
                        item.setForeground(QColor(255, 0, 0))
                    elif row[col] == "USA":
                        item.setFont(bold)
                        item.setForeground(QColor(0, 0, 255))
                elif col == "Code" or col == "Serial number":
                    self.setColumnWidth(j, 140)
                elif col == "Year":
                    self.setColumnWidth(j, 40)
                elif col in ["Game", "Console", "Accessory", "Box", "Manual"]:
                    self.setColumnWidth(j, 70)
                    item.setTextAlignment(Qt.AlignCenter)
                    if row[col] == "Yes":
                        if "In collection" not in self._items[i].keys():
                            self._items[i]["In collection"] = True  # Owned status for item
                        item.setFont(bold)
                        item.setForeground(QColor(0, 255, 0))
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        item.setCheckState(Qt.Checked)
                    elif row[col] == "No":
                        if "In collection" not in self._items[i].keys():
                            self._items[i]["In collection"] = False  # Owned status for item
                        item.setFont(bold)
                        item.setForeground(QColor(255, 0, 0))
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        item.setCheckState(Qt.Unchecked)

                self.setItem(i, j, item)

        if len(self._tableData) < 1:  # Again, for empty tables
            for i, key in enumerate(self._tableData):
                if key == "Platform":
                    self.sortByColumn(i, Qt.AscendingOrder)
                    break
        else:
            for i, key in enumerate(self._tableData[0]):
                if key == "Platform":
                    self.sortByColumn(i, Qt.AscendingOrder)
                    break

        self.setSortingEnabled(True)

    def _resize(self):
        self.resizeRowsToContents()

    def _updateTable(self):
        self._isUpdating = True  # So _onEdit doesn't get angry
        self.setRowCount(0)
        self._tableDB.saveData(self._tableData)
        self._tableData = self._tableDB.connect()
        self._populateTable()
        self.searchTable("")
        self._isUpdating = False
        self.updated.emit()

    def addData(self, newData):
        if isinstance(newData, list):
            for data in newData:
                self._tableData.append(data)
        elif isinstance(newData, OrderedDict):
            self._tableData.append(newData)

        self._updateTable()

    def deleteData(self, rows):
        count = 0  # Since number of rows in tableData shrinks
        for row in rows:
            rowToDelete = 0  # Row in database file to delete, rather than row in table
            for col, key in enumerate(self._tableData[0].keys()):
                if key == "Name":
                    for itemRow in range(len(self._items)):
                        if self.item(row, col).text() in self._items[itemRow]["Name"]:
                            rowToDelete = self._items[itemRow]["Row"]
                            break

            del self._tableData[rowToDelete - count]
            count += 1

        self._updateTable()

    def deleteNotOwned(self):
        count = 0
        for row in self._items:
            for col in row:
                if col == "In collection" and not row[col]:
                    del self._tableData[row["Row"] - count]
                    count += 1

        self._updateTable()

    def getData(self):
        return self._tableData

    def getDataLength(self):
        return len(self._tableData)

    def getOwnedCount(self):
        """Returns number of owned items in table."""

        ownedCount = 0

        for row in self._items:
            for col in row:
                if col == "In collection" and row[col]:  # row[col] = True/False
                    ownedCount += 1
                    break

        return ownedCount

    def getOwnedItems(self):
        """Returns the owned items in table"""

        items = []

        for row in self._items:
            for col in row:
                if col == "In collection" and row[col]:
                    items.append(row)

        return items

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def saveData(self):
        self._tableDB.connect()
        self._updateTable()

    def searchTable(self, text):
        """Searches the table for 'text'. Rows not matching 'text' are hidden.
           If self._hideNotOwned is True, then also filter out the not owned items.
           It returns the number of rows it has found."""

        # TODO: Understand why this works

        # TODO: Fix issue with table not updating when user erases letters

        rowCount = 0

        # This is a confusing name with the current logic for hiding rows,
        # but I don't quite understand why the logic works this way... :D
        # Sometimes the rows not in rowsToShow are hidden as expected,
        # and sometimes it's the opposite!
        rowsToShow = set()

        if self._hideNotOwned:
            ownedItems = []
            for i, row in enumerate(self._items):
                for col in row:
                    if col == "In collection" and row[col]:
                        ownedItems.append(self._items[i]["Name"])

            for row in range(self.rowCount()):
                match = False
                for col in range(self.columnCount()):
                    item = self.item(row, col).text()
                    if item in ownedItems:
                        match = True
                        rowsToShow.add(row)
                        break
                self.setRowHidden(row, not match)

        if text == "":
            if self._hideNotOwned:
                for row in range(self.rowCount()):
                    if row not in rowsToShow:
                        self.setRowHidden(row, True)
                rowCount = len(rowsToShow)
            else:
                for row in range(self.rowCount()):
                    self.setRowHidden(row, False)
                rowCount = self.rowCount()
        else:
            if self._hideNotOwned:
                searchItems = self.findItems(text, Qt.MatchContains)
                for item in searchItems:
                    if self.indexFromItem(item).row() in rowsToShow:
                        # This doesn't make sense but it works
                        rowsToShow.discard(self.indexFromItem(item).row())

                for row in range(self.rowCount()):
                    # I don't understand why this works the opposite way from when 'text' is empty
                    if row in rowsToShow:
                        self.setRowHidden(row, True)
                    else:
                        rowCount += 1
                rowCount -= 1  # It seems to count one more than necessary?
            else:
                searchItems = self.findItems(text, Qt.MatchContains)
                for item in searchItems:
                    rowsToShow.add(self.indexFromItem(item).row())
                for row in range(self.rowCount()):
                    if row not in rowsToShow:
                        self.setRowHidden(row, True)
                rowCount = len(rowsToShow)

        self.resizeRowsToContents()

        return rowCount

    def searchTableData(self, key="", value=""):
        """Searches the raw table orderedDict structure for data and returns
           the number of matches. Can search for key, value, or both.
           Returns the number of matches."""

        matchCount = 0
        if len(self._tableData) < 1:  # Empty table
            return 0
        else:
            keys = self._tableData[0].keys()

        # Searches for specific value in specific key
        if not key == "" and not value == "":
            for row in self._tableData:
                match = False
                for col in keys:
                    if col == key and row[col] == value:
                        match = True
                        matchCount += 1
                        break
        # Searches for specific value in all keys
        elif key == "" and not value == "":
            for row in self._tableData:
                match = False
                for col in keys:
                    if row[col] == value:
                        match = True
                        matchCount += 1
                        break
        # Searches for all values in specific key
        elif not key == "" and value == "":
            for row in self._tableData:
                match = False
                for col in keys:
                    if col == key:
                        match = True
                        matchCount += 1
                        break

        return matchCount

    def setHideNotOwned(self, hide):
        self._hideNotOwned = hide
        self.searchTable("")
        #self.resizeRowsToContents()

    def isHideNotOwned(self):
        return self._hideNotOwned


class SqlTable(QTableView):
    """
    Re-implementation of Table class using SQLITE rather than CSV
    """

    resized = Signal()

    def __init__(self, tableName, db):
        super().__init__()

        self.resized.connect(self.resizeRowsToContents)

        assert tableName in ("games", "consoles", "accessories")

        self.db = db

        self.model = TableModel(self, self.db)
        self.model.setTable(tableName)
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Platform")
        self.model.setHeaderData(2, Qt.Horizontal, "Name")
        self.model.setHeaderData(3, Qt.Horizontal, "Region")
        if tableName == "games":
            self.model.setHeaderData(4, Qt.Horizontal, "Code")
            self.model.setHeaderData(5, Qt.Horizontal, "Game")
            self.setItemDelegateForColumn(5, CheckboxDelegate("Game", parent=self))
            self.model.setHeaderData(6, Qt.Horizontal, "Box")
            self.setItemDelegateForColumn(6, CheckboxDelegate("Box", parent=self))
            self.model.setHeaderData(7, Qt.Horizontal, "Manual")
            self.setItemDelegateForColumn(7, CheckboxDelegate("Manual", parent=self))
            self.model.setHeaderData(8, Qt.Horizontal, "Year")
            self.model.setHeaderData(9, Qt.Horizontal, "Comment")
        elif tableName == "consoles":
            self.model.setHeaderData(4, Qt.Horizontal, "Country")
            self.model.setHeaderData(5, Qt.Horizontal, "Serial number")
            self.model.setHeaderData(6, Qt.Horizontal, "Console")
            self.setItemDelegateForColumn(6, CheckboxDelegate("Console", parent=self))
            self.model.setHeaderData(7, Qt.Horizontal, "Box")
            self.setItemDelegateForColumn(7, CheckboxDelegate("Box", parent=self))
            self.model.setHeaderData(8, Qt.Horizontal, "Manual")
            self.setItemDelegateForColumn(8, CheckboxDelegate("Manual", parent=self))
            self.model.setHeaderData(9, Qt.Horizontal, "Year")
            self.model.setHeaderData(10, Qt.Horizontal, "Comment")
        elif tableName == "accessories":
            self.model.setHeaderData(4, Qt.Horizontal, "Country")
            self.model.setHeaderData(5, Qt.Horizontal, "Accessory")
            self.setItemDelegateForColumn(5, CheckboxDelegate("Accessory", parent=self))
            self.model.setHeaderData(6, Qt.Horizontal, "Box")
            self.setItemDelegateForColumn(6, CheckboxDelegate("Box", parent=self))
            self.model.setHeaderData(7, Qt.Horizontal, "Manual")
            self.setItemDelegateForColumn(7, CheckboxDelegate("Manual", parent=self))
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
            elif self.model.headerData(column, Qt.Horizontal) == "Region":
                self.setColumnWidth(column, 85)
            elif self.model.headerData(column, Qt.Horizontal) in ("Code", "Country", "Serial number"):
                self.setColumnWidth(column, 140)
            elif self.model.headerData(column, Qt.Horizontal) == "Year":
                self.setColumnWidth(column, 40)
            elif self.model.headerData(column, Qt.Horizontal) in ("Game", "Console", "Accessory", "Box", "Manual"):
                self.setColumnWidth(column, 70)

        self.verticalHeader().setVisible(False)  # Don't show row headers
        #self.setSortingEnabled(True)
        self.sortByColumn(1, Qt.AscendingOrder)  # Sort by platform
        self.setColumnHidden(0, True)  # Don't show ID field
        self.resizeRowsToContents()

    def addData(self, dataDict):
        itemID = self.model.rowCount()
        newRecord = self.model.record()
        newRecord.setValue("ID", itemID)
        newRecord.setValue("Platform", dataDict["Platform"])
        newRecord.setValue("Name", dataDict["Name"])
        newRecord.setValue("Region", dataDict["Region"])
        if self.model.tableName() == "games":
            newRecord.setValue("Code", dataDict["Code"])
            newRecord.setValue("Game", dataDict["Game"])
        elif self.model.tableName() == "consoles":
            newRecord.setValue("Country", dataDict["Country"])
            newRecord.setValue("Serial number", dataDict["Serial number"])
            newRecord.setValue("Console", dataDict["Console"])
        elif self.model.tableName() == "accessories":
            newRecord.setValue("Country", dataDict["Country"])
            newRecord.setValue("Accessory", dataDict["Accessory"])
        newRecord.setValue("Box", dataDict["Box"])
        newRecord.setValue("Manual", dataDict["Manual"])
        newRecord.setValue("Year", dataDict["Year"])
        newRecord.setValue("Comment", dataDict["Comment"])

        if not self.model.insertRecord(-1, newRecord):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Error")
            msgBox.setText("Error adding to database: " + self.model.query().lastError().text())
            msgBox.exec_()

        self.sortByColumn(1, Qt.AscendingOrder)

    def itemsInPlatform(self, platform):
        count = 0
        item = "Game" if self.model.tableName() == "games" else\
            "Console" if self.model.tableName() == "consoles" else "Accessory"

        query = QSqlQuery()
        query.exec_("SELECT * FROM {} WHERE Platform='{}'"
                    "AND ({}='Yes' OR Box='Yes' OR Manual='Yes')".format(
            self.model.tableName(), platform, item))
        while query.next():
            count += 1

        return count

    def ownedCount(self):
        count = 0
        item = "Game" if self.model.tableName() == "games" else\
            "Console" if self.model.tableName() == "consoles" else "Accessory"

        query = QSqlQuery()
        query.exec_("SELECT * FROM {} WHERE {}='Yes' OR Box='Yes' OR Manual='Yes'".format(
            self.model.tableName(), item))
        while query.next():
            count += 1

        return count

    def platforms(self):
        platforms = set()

        query = QSqlQuery()
        query.exec_("SELECT Platform FROM {}".format(self.model.tableName()))
        while query.next():
            platforms.add(query.value(0))

        return platforms

    def resizeEvent(self, event):
        """
        Currently doesn't seem to trigger when pressing window manager minimize/maximize button
        """

        self.resized.emit()
        return super().resizeEvent(event)

    def test(self):
        pass

    def searchTable(self, term):
        items = self.findItems(term, Qt.MatchContains)
        for item in items:
            print(item.text())
