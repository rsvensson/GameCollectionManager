from collections import OrderedDict

from PySide2.QtCore import Qt, Signal, QModelIndex, QItemSelectionModel
from PySide2.QtGui import QKeyEvent, QMouseEvent, QFont, QColor
from PySide2.QtSql import QSqlTableModel, QSqlQuery
from PySide2.QtWidgets import QAbstractItemView, QTableView
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

        self.hideNotOwned = True
        self._table = tableName
        self._itemType = "Game" if self._table == "games"\
            else "Console" if self._table == "consoles"\
            else "Accessory"

        self.model = TableModel(self, db)
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

        db = self.model.database()
        table = self._table

        gamesColumns = ["Platform", "Name", "Region", "Code", "Game", "Box", "Manual",
                        "Year", "Genre", "Comment", "Publisher", "Developer", "Platforms"]
        consolesColumns = ["Platform", "Name", "Region", "Country", "Serial number",
                           "Console", "Box", "Manual", "Year", "Comment"]
        accessoriesColumns = ["Platform", "Name", "Region", "Country", "Accessory",
                              "Box", "Manual", "Year", "Comment"]

        if isinstance(newData, list):
            for data in newData:
                if table == "games":
                    record = self.model.record()
                    record.remove(record.indexOf("ID"))
                    for i in gamesColumns:
                        record.setValue(i, data[i])

                    if self.model.insertRecord(-1, record):
                        pass
                    else:
                        db.rollback()
                elif table == "consoles":
                    record = self.model.record()
                    record.remove(record.indexOf("ID"))
                    for i in consolesColumns:
                        record.setValue(i, data[i])

                    if self.model.insertRecord(-1, record):
                        pass
                    else:
                        db.rollback()
                elif table == "accessories":
                    record = self.model.record()
                    record.remove(record.indexOf("ID"))
                    for i in accessoriesColumns:
                        record.setValue(i, data[i])

                    if self.model.insertRecord(-1, record):
                        pass
                    else:
                        db.rollback()

        elif isinstance(newData, OrderedDict) or isinstance(newData, dict):
            if table == "games":
                record = self.model.record()
                record.remove(record.indexOf("ID"))
                for i in gamesColumns:
                    record.setValue(i, newData[i])

                if self.model.insertRecord(-1, record):
                    pass
                else:
                    db.rollback()

            elif table == "consoles":
                record = self.model.record()
                record.remove(record.indexOf("ID"))
                for i in consolesColumns:
                    record.setValue(i, newData[i])

                if self.model.insertRecord(-1, record):
                    pass
                else:
                    db.rollback()
            elif table == "accessories":
                record = self.model.record()
                record.remove(record.indexOf("ID"))
                for i in accessoriesColumns:
                    record.setValue(i, newData[i])

                if self.model.insertRecord(-1, record):
                    pass
                else:
                    db.rollback()

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

    def rowInfo(self):
        row = self.currentIndex().row()
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

    def updateData(self, data: dict):
        currentRow = self.currentIndex().row()

        if self._table == "games":
            codeIndex = self.model.index(currentRow, 4)
            yearIndex = self.model.index(currentRow, 8)
            genreIndex = self.model.index(currentRow, 9)
            publisherIndex = self.model.index(currentRow, 11)
            developerIndex = self.model.index(currentRow, 12)
            platformsIndex = self.model.index(currentRow, 13)
            self.model.setData(codeIndex, data["code"])
            self.model.setData(yearIndex, data["year"])
            self.model.setData(genreIndex, data["genre"])
            self.model.setData(publisherIndex, data["publisher"])
            self.model.setData(developerIndex, data["developer"])
            self.model.setData(platformsIndex, data["platforms"])


class TableModel(QSqlTableModel):
    """
    Subclassing QSqlTableModel to be able to customize data in our cells
    """

    def __init__(self, *args, **kwargs):
        super(TableModel, self).__init__(*args, **kwargs)

    def flags(self, index):
        if self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory",
                                                              "Box", "Manual"):
            return super().flags(index) | Qt.ItemIsUserCheckable
        else:
            return super().flags(index)

    def data(self, index, role=Qt.DisplayRole):
        # Handle setting our checkboxes
        if (role == Qt.CheckStateRole or role == Qt.DisplayRole)\
            and self.headerData(index.column(), Qt.Horizontal) in\
                ("Game", "Console", "Accessory", "Box", "Manual"):

            if role == Qt.CheckStateRole:
                if index.data(Qt.EditRole) == "Yes":
                    return Qt.Checked
                elif index.data(Qt.EditRole) == "No":
                    return Qt.Unchecked
            elif role == Qt.DisplayRole:
                # Display text next to checkboxes
                return super().data(index, role)
                # No text
                # return ""
        # Bold fonts
        elif role == Qt.FontRole and self.headerData(index.column(), Qt.Horizontal) in \
                ("Region", "Country", "Game", "Console", "Accessory", "Box", "Manual"):
            font = QFont()
            font.setBold(True)
            return font
        # Set foreground color
        elif role == Qt.ForegroundRole:
            if self.headerData(index.column(), Qt.Horizontal) == "Region":
                if index.data() in ("PAL", "PAL A", "PAL B", "Europe"):
                    return QColor(255, 255, 0)
                elif index.data() in ("NTSC (JP)", "Japan"):
                    return QColor(255, 0, 0)
                elif index.data() in ("NTSC (NA)", "North America"):
                    return QColor(0, 0, 255)
            elif self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory",
                                                                    "Box", "Manual"):
                if index.data(Qt.EditRole) == "Yes":
                    return QColor(0, 255, 0)
                elif index.data(Qt.EditRole) == "No":
                    return QColor(255, 0, 0)
        # Set text alignment
        elif role == Qt.TextAlignmentRole \
                and self.headerData(index.column(), Qt.Horizontal) in ("Region", "Country"):
            return Qt.AlignCenter
        # Display the cell data in tooltip
        #elif role == Qt.ToolTipRole:
        #    return super().data(index, Qt.DisplayRole)

        return super().data(index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole\
                and self.headerData(index.column(), Qt.Horizontal) in \
                ("Game", "Console", "Accessory", "Box", "Manual"):
            data = "Yes" if value == Qt.Checked else "No"
            return super().setData(index, data, Qt.EditRole)
        else:
            return super().setData(index, value, role)