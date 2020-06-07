from random import randint
from os import path

from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QListWidget, QAbstractItemView, QPushButton, QHBoxLayout, QVBoxLayout, \
    QGridLayout, QCheckBox


class Randomizer(QWidget):
    """A game randomizer for selecting a random game to play
       from the user's collection. User can select which
       platforms to choose from.
       gamesData: Raw table data in list of orderedDicts"""

    def __init__(self, gamesData: list, platformsData: list, genresData: list):
        super(Randomizer, self).__init__()

        self._consoleItems = platformsData
        self._genreItems = genresData
        self._gamesData = gamesData
        self._games = []  # For holding the games to randomize
        self._gameCount = 0
        self._coverdir = path.join("data", "images", "covers")

        self.consoleLabel = QLabel("Platforms")
        self.consoleList = QListWidget()
        self.consoleList.addItems(self._consoleItems)
        self.consoleList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.consoleList.setMaximumWidth(350)
        self.consoleList.itemClicked.connect(self._updateGameCount)

        self.genreLabel = QLabel("Genres")
        self.genreMatchExclusiveCB = QCheckBox("Match exclusive")
        self.genreMatchExclusiveCB.setToolTip("Only match games which exclusively contain the selected genres.")
        self.genreMatchExclusiveCB.setChecked(False)
        self.genreMatchExclusiveCB.stateChanged.connect(self._updateGameCount)
        self.genreList = QListWidget()
        self.genreList.addItems(self._genreItems)
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

        # Cover image
        self._cover = QLabel()
        self._cover.setVisible(False)
        self._cover.setAlignment(Qt.AlignCenter)
        p = QPixmap(path.join(self._coverdir, "none.png"))
        w = self._cover.width()
        h = self._cover.height()
        self._cover.setPixmap(p.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self._hboxButtons = QHBoxLayout()
        self._vboxLists = QVBoxLayout()
        self._vboxConsoles = QVBoxLayout()
        self._hboxGenres = QHBoxLayout()
        self._vboxGenres = QVBoxLayout()
        self._vboxResult = QVBoxLayout()
        self._grid = QGridLayout()
        self._hboxButtons.addWidget(self.btnAll, 0)
        self._hboxButtons.addWidget(self.btnNone, 0)
        self._hboxButtons.addWidget(self._btnRnd, 0)
        self._vboxConsoles.addWidget(self.consoleLabel, 0)
        self._vboxConsoles.addWidget(self.consoleList, 1)
        self._hboxGenres.addWidget(self.genreLabel, 0)
        self._hboxGenres.addWidget(self.genreMatchExclusiveCB, 0)
        self._vboxGenres.addWidget(self.genreList, 1)
        self._vboxLists.addSpacing(10)
        self._vboxLists.addLayout(self._vboxConsoles, 1)
        self._vboxLists.addSpacing(10)
        self._vboxLists.addLayout(self._hboxGenres, 0)
        self._vboxLists.addLayout(self._vboxGenres, 1)
        self._vboxResult.addStretch(3)
        self._vboxResult.addWidget(self._lblPlay, 0)
        self._vboxResult.addWidget(self._lblTitle, 0)
        self._vboxResult.addSpacing(50)
        self._vboxResult.addWidget(self._cover, 0)
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

        if len(self._games) > 0 and (len(platforms) > 0 or len(genres) > 0):
            choice = randint(0, len(self._games) - 1)
            self._lblPlay.setText("You will play:")
            self._lblTitle.setText(f"{self._games[choice]['Name']}" if len(platforms) == 1 else
                                   f"{self._games[choice]['Name']} [{self._games[choice]['Platform']}]")
            # Cover image
            cover = str(self._games[choice]['ID']) + ".jpg"
            if path.exists(path.join(self._coverdir, cover)):
                # Update cover image if the game has one
                pixmap = path.join(self._coverdir, cover)
                self._cover.setVisible(True)
            else:
                pixmap = path.join(self._coverdir, "none.png")
                self._cover.setVisible(False)
            p = QPixmap(pixmap)
            w = self._cover.width()
            h = self._cover.height()
            self._cover.setPixmap(p.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif len(self._games) == 0 and (len(platforms) > 0 or len(genres) > 0):
            self._lblPlay.setText("")
            self._lblTitle.setText("No games found with those criteria.")
            self._cover.setVisible(False)
        else:
            self._lblPlay.setText("")
            self._lblTitle.setText("Select at least one console or genre...")
            self._cover.setVisible(False)

    def _updateGameCount(self):
        platforms, genres = self._getSelectedItems()
        self._gameCount = 0
        self._games = []

        if len(platforms) > 0 or len(genres) > 0:
            for row in self._gamesData:
                if len(platforms) > 0 and len(genres) > 0:
                    if row["Platform"] in platforms:
                        if self.genreMatchExclusiveCB.isChecked():
                            count = 0
                            for genre in row["Genre"].split(", "):
                                if genre in genres:
                                    count += 1
                                else:  # Not exclusive
                                    count = 0
                                    break
                            if count == len(genres):
                                self._gameCount += 1
                                self._games.append(row)
                        else:
                            for genre in row["Genre"].split(", "):
                                if genre in genres:
                                    self._gameCount += 1
                                    self._games.append(row)
                                    break  # We only need to match with one genre
                elif len(platforms) > 0 and len(genres) == 0:
                    if row["Platform"] in platforms:
                        self._gameCount += 1
                        self._games.append(row)
                elif len(platforms) == 0 and len(genres) > 0:
                    if self.genreMatchExclusiveCB.isChecked():
                        count = 0
                        for genre in row["Genre"].split(", "):
                            if genre in genres:
                                count += 1
                            else:  # Not exclusive
                                count = 0
                                break
                        if count == len(genres):
                            self._gameCount += 1
                            self._games.append(row)
                    else:
                        for genre in row["Genre"].split(", "):
                            if genre in genres:
                                self._gameCount += 1
                                self._games.append(row)
                                break  # We only need to match with one genre

    def gameCount(self) -> int:
        return self._gameCount

    def updateLists(self, gamesData: list, platformsData: list, genresData: list):
        self._gamesData = gamesData
        self._consoleItems = platformsData
        self._genreItems = genresData
        self.consoleList.clear()
        self.genreList.clear()

        self.consoleList.addItems(sorted(self._consoleItems, key=str.lower))
        self.genreList.addItems(sorted(self._genreItems, key=str.lower))
