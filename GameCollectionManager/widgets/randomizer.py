from random import randint

from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QLabel, QListWidget, QAbstractItemView, QPushButton, QHBoxLayout, QVBoxLayout, \
    QGridLayout


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

    def updateGenres(self, genreData: dict):
        self.genreList.clear()
        self._genreItems.add(genreData["genre"])
        self.genreList.addItems(sorted(self._genreItems, key=str.lower))

    def updatePlatforms(self, gamesData: list):
        self._gamesData.clear()
        self.consoleList.clear()
        self._gamesData = gamesData

        for row in self._gamesData:
            self._consoleItems.add(row["Platform"])
        self.consoleList.addItems(sorted(self._consoleItems, key=str.lower))
