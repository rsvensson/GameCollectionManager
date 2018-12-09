from PySide2.QtWidgets import QWidget, QDialog,\
    QGridLayout, QVBoxLayout, QHBoxLayout,\
    QTableWidget, QTableWidgetItem, QDesktopWidget,\
    QLineEdit, QPushButton, QComboBox, QCheckBox, QLabel,\
    QListWidget, QAbstractItemView, QInputDialog, QMessageBox
from PySide2.QtGui import QColor, QFont
from PySide2.QtCore import Qt, QSize, Signal
from collections import OrderedDict
from random import randint

class InputWindow(QDialog):
    """Window where user can enter new data into a table.
       It returns the data formatted into an OrderedDict.
       platforms: the platforms from the currently loaded
                  collection."""

    def __init__(self, platforms, parent=None):
        super(InputWindow, self).__init__(parent=parent)

        self.setContentsMargins(5, 5, 5, 5)

        self.dataTypes = ["Game", "Console", "Accessory"]
        self.dataTypeLabel = QLabel()
        self.dataTypeLabel.setText("Type\t ")
        self.dataType = QComboBox()
        self.dataType.addItems(self.dataTypes)
        self.dataType.currentIndexChanged.connect(self._changeWidgets)

        self.nameLabel = QLabel()
        self.nameLabel.setText("Name\t ")
        self.name = QLineEdit()

        self.platformLabel = QLabel()
        self.platformLabel.setText("Platform\t ")
        self.platform = QComboBox()
        self.platform.addItems(platforms if len(platforms) > 0 else " ")
        self.platform.addItem("New")
        self.platform.currentIndexChanged.connect(self._addPlatform)

        self.regionLabel = QLabel()
        self.regionLabel.setText("Region\t ")
        self.region = QLineEdit()

        self.countryLabel = QLabel()
        self.countryLabel.setText("Country\t ")
        self.country = QLineEdit()
        self.country.setEnabled(False)

        self.codeLabel = QLabel()
        self.codeLabel.setText("Code\t ")
        self.code = QLineEdit()

        self.itemLabel = QLabel()
        self.itemLabel.setText("Game")
        self.item = QCheckBox()

        self.boxLabel = QLabel()
        self.boxLabel.setText("Box")
        self.box = QCheckBox()

        self.manualLabel = QLabel()
        self.manualLabel.setText("Manual")
        self.manual = QCheckBox()

        self.commentLabel = QLabel()
        self.commentLabel.setText("Comment ")
        self.comment = QLineEdit()

        self.okButton = QPushButton()
        self.okButton.setText("OK")
        self.okButton.setMaximumSize(self.okButton.sizeHint())
        self.okButton.clicked.connect(self.accept)
        self.cnclButton = QPushButton()
        self.cnclButton.setText("Cancel")
        self.cnclButton.setMaximumSize(self.cnclButton.sizeHint())
        self.cnclButton.clicked.connect(self.reject)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch()
        self.hboxType = QHBoxLayout()
        self.hboxType.addStretch()
        self.hboxName = QHBoxLayout()
        self.hboxName.addStretch()
        self.hboxPlatform = QHBoxLayout()
        self.hboxRegion = QHBoxLayout()
        self.hboxRegion.addStretch()
        self.hboxCode = QHBoxLayout()
        self.hboxCode.addStretch()
        self.hboxBoxMan = QHBoxLayout()
        self.hboxComment = QHBoxLayout()
        self.hboxComment.addStretch()
        self.hboxBtn = QHBoxLayout()
        self.hboxBtn.addStretch()

        self.hboxType.addWidget(self.dataTypeLabel, 0)
        self.hboxType.addWidget(self.dataType, 1)
        self.hboxName.addWidget(self.nameLabel, 0)
        self.hboxName.addWidget(self.name, 1)
        self.hboxPlatform.addWidget(self.platformLabel, 0)
        self.hboxPlatform.addWidget(self.platform, 1)
        self.hboxRegion.addWidget(self.regionLabel, 0)
        self.hboxRegion.addWidget(self.region, 1)
        self.hboxCode.addWidget(self.codeLabel, 0)
        self.hboxCode.addWidget(self.code, 1)
        self.hboxComment.addWidget(self.commentLabel, 0)
        self.hboxComment.addWidget(self.comment, 1)
        self.hboxBoxMan.addStretch(10)
        self.hboxBoxMan.addWidget(self.itemLabel, 0)
        self.hboxBoxMan.addWidget(self.item, 1)
        self.hboxBoxMan.addStretch(5)
        self.hboxBoxMan.addWidget(self.boxLabel, 2)
        self.hboxBoxMan.addWidget(self.box, 3)
        self.hboxBoxMan.addStretch(5)
        self.hboxBoxMan.addWidget(self.manualLabel, 4)
        self.hboxBoxMan.addWidget(self.manual, 5)
        self.hboxBoxMan.addStretch(10)
        self.hboxBtn.addWidget(self.cnclButton, 0)
        self.hboxBtn.addWidget(self.okButton, 1)

        self.vbox.addLayout(self.hboxType, 0)
        self.vbox.addLayout(self.hboxName, 1)
        self.vbox.addLayout(self.hboxPlatform, 2)
        self.vbox.addLayout(self.hboxRegion, 3)
        self.vbox.addLayout(self.hboxCode, 4)
        self.vbox.addLayout(self.hboxComment, 5)
        self.vbox.addLayout(self.hboxBoxMan, 6)
        self.vbox.addLayout(self.hboxBtn, 7)

        self.setLayout(self.vbox)

        self.setWindowTitle("Add to collection")
        self.setFixedSize(QSize(500, 280))
        self._center()

    def _addPlatform(self):
        if self.platform.currentText() == "New":
            platform, ok = QInputDialog.getText(self, "Add platform",
                                                "Platform name:")
            if ok and platform is not "" and not platform.isspace():
                lastIndex = self.platform.count()
                self.platform.addItem(platform)
                self.platform.setCurrentIndex(lastIndex)
                self.platform.removeItem(self.platform.findText(" "))  # Remove the temp empty item if any

    def _center(self):
        """Centers window on screen"""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _changeWidgets(self):
        """Changes the label widgets based on what type of data is being entered"""

        if self.dataType.currentIndex() == 0:
            self.code.setEnabled(True)
            self.country.setEnabled(False)
            self.codeLabel.setText("Code\t ")
            self.itemLabel.setText("Game")
        elif self.dataType.currentIndex() == 1:
            self.code.setEnabled(True)
            self.country.setEnabled(True)
            self.codeLabel.setText("Serial No\t ")
            self.itemLabel.setText("Console")
        elif self.dataType.currentIndex() == 2:
            self.country.setEnabled(True)
            self.code.setEnabled(False)
            self.itemLabel.setText("Accessory")

    def returnData(self):
        data = None

        if self.dataType.currentIndex() == 0:
            data = OrderedDict([('Platform', '{}'.format(self.platform.currentText())),
                                ('Name', '{}'.format(self.name.text())),
                                ('Region', '{}'.format(self.region.text())),
                                ('Code', '{}'.format(self.code.text())),
                                ('Game', '{}'.format('Yes' if self.item.isChecked() else 'No')),
                                ('Box', '{}'.format('Yes' if self.box.isChecked() else 'No')),
                                ('Manual', '{}'.format('Yes' if self.manual.isChecked() else 'No')),
                                ('Comment', '{}'.format(self.comment.text()))])

        elif self.dataType.currentIndex() == 1:
            data = OrderedDict([('Platform', '{}'.format(self.platform.currentText())),
                                ('Name', '{}'.format(self.name.text())),
                                ('Region', '{}'.format(self.region.text())),
                                ('Country', '{}'.format(self.country.text())),
                                ('Serial number', '{}'.format(self.code.text())),
                                ('Console', '{}'.format('Yes' if self.item.isChecked() else 'No')),
                                ('Box', '{}'.format('Yes' if self.box.isChecked() else 'No')),
                                ('Manual', '{}'.format('Yes' if self.manual.isChecked() else 'No')),
                                ('Comment', '{}'.format(self.comment.text()))])

        elif self.dataType.currentIndex() == 2:
            data = OrderedDict([('Platform', '{}'.format(self.platform.currentText())),
                                ('Name', '{}'.format(self.name.text())),
                                ('Region', '{}'.format(self.region.text())),
                                ('Country', '{}'.format(self.country.text())),
                                ('Accessory', '{}'.format('Yes' if self.item.isChecked() else 'No')),
                                ('Box', '{}'.format('Yes' if self.box.isChecked() else 'No')),
                                ('Manual', '{}'.format('Yes' if self.manual.isChecked() else 'No')),
                                ('Comment', '{}'.format(self.comment.text()))])
        if data['Platform'] == "" or data['Platform'].isspace():
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("<h2>Invalid platform</h2>")
                msgBox.setInformativeText("Can't add empty string or whitespace "+
                                          "as platform name. Aborting.")

        return data


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
            self.lblTitle.setText("{}".format(games[choice]["Game"]) if len(platforms) == 1 else
                                  "{} [{}]".format(games[choice]["Game"], games[choice]["Platform"]))
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
        """tableDB: A 'Database' (csv/tsv) object"""

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
                    if row[col] == "NTSC (JP)":
                        item.setForeground(QColor(255, 0, 0))
                    if row[col] == "NTSC (NA)":
                        item.setForeground(QColor(0, 0, 255))
                    if "PAL" in row[col]:
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

    def getData(self):
        return self._tableData

    def getOwned(self):
        """Returns number of owned items in table."""

        ownedItems = 0

        for row in self._items:
            for col in row:
                if col == "In collection" and row[col]:  # row[col] = True/False
                    ownedItems += 1
                    break

        return ownedItems

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

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
