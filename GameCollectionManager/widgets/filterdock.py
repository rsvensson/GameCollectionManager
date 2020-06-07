from collections import defaultdict

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QDockWidget, QWidget, QListWidget, QHBoxLayout, \
    QLabel, QPushButton, QAbstractItemView, QVBoxLayout, QGroupBox, QCheckBox


class FilterDock(QDockWidget):

    def __init__(self, platforms, regions, genres, years):
        super(FilterDock, self).__init__()

        # QDockWidget settings
        self.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetClosable)
        self.setFixedHeight(150)
        self.setVisible(False)
        self.setWindowTitle("Filter options")

        # The selected items for each widget are saved in a set-dictionary
        self._selections = defaultdict(set)

        #  Widget settings
        # Platform widgets
        self._platformLabel = QLabel("Platform")
        self._platforms = QListWidget()
        self._platforms.addItems(platforms)
        self._platforms.setSelectionMode(QAbstractItemView.MultiSelection)
        self._platforms.setMaximumWidth(200)
        self._platformVBox = QVBoxLayout()
        self._platformVBox.addWidget(self._platformLabel, 0)
        self._platformVBox.addWidget(self._platforms, 1)

        # Region widgets
        self._regionLabel = QLabel("Region")
        self._regions = QListWidget()
        self._regions.addItems(regions)
        self._regions.setSelectionMode(QAbstractItemView.MultiSelection)
        self._regions.setMaximumWidth(200)
        self._regionVBox = QVBoxLayout()
        self._regionVBox.addWidget(self._regionLabel, 0)
        self._regionVBox.addWidget(self._regions, 1)

        # Genre widgets
        self._genreLabel = QLabel("Genre")
        self._genres = QListWidget()
        self._genres.addItems(genres)
        self._genres.setSelectionMode(QAbstractItemView.MultiSelection)
        self._genres.setMaximumWidth(300)
        self._genreVBox = QVBoxLayout()
        self._genreVBox.addWidget(self._genreLabel, 0)
        self._genreVBox.addWidget(self._genres, 1)

        # Year widgets
        self._yearLabel = QLabel("Year")
        self._years = QListWidget()
        self._years.addItems(years)
        self._years.setSelectionMode(QAbstractItemView.MultiSelection)
        self._years.setMaximumWidth(75)
        self._yearsVbox = QVBoxLayout()
        self._yearsVbox.addWidget(self._yearLabel, 0)
        self._yearsVbox.addWidget(self._years, 1)

        # Inventory widgets
        self._itemType = {1: "Game", 2: "Console", 3: "Accessory"}
        self._item = QCheckBox(self._itemType[1])
        self._item.setTristate(True)
        self._item.setCheckState(Qt.PartiallyChecked)
        self._manual = QCheckBox("Manual")
        self._manual.setTristate(True)
        self._manual.setCheckState(Qt.PartiallyChecked)
        self._box = QCheckBox("Box")
        self._box.setTristate(True)
        self._box.setCheckState(Qt.PartiallyChecked)
        self._inventoryLabelsVBox = QVBoxLayout()
        self._inventorySelectionsVBox = QVBoxLayout()
        self._inventorySelectionsVBox.addStretch(3)
        self._inventorySelectionsVBox.addWidget(self._item, 0)
        self._inventorySelectionsVBox.addWidget(self._box, 1)
        self._inventorySelectionsVBox.addWidget(self._manual, 2)
        self._inventorySelectionsVBox.setAlignment(Qt.AlignLeft)
        self._haveHBox = QHBoxLayout()
        self._haveHBox.addLayout(self._inventoryLabelsVBox, 0)
        self._haveHBox.addLayout(self._inventorySelectionsVBox, 1)
        self._inventoryGroup = QGroupBox("Inventory")
        self._inventoryGroup.setMaximumWidth(120)
        self._inventoryGroup.setLayout(self._haveHBox)

        # Clear and Apply button widgets
        self._clearBtn = QPushButton("Clear selection")
        self._clearBtn.setMaximumSize(self._clearBtn.sizeHint())
        self._clearBtn.clicked.connect(self._clearFilters)
        self._btnHBox = QHBoxLayout()
        self._btnHBox.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self._btnHBox.addWidget(self._clearBtn, 0)

        # General layout
        mainHBox = QHBoxLayout()
        mainHBox.setAlignment(Qt.AlignLeft)
        mainHBox.addLayout(self._platformVBox, 0)
        mainHBox.addLayout(self._regionVBox, 0)
        mainHBox.addLayout(self._genreVBox, 0)
        mainHBox.addLayout(self._yearsVbox, 0)
        mainHBox.addWidget(self._inventoryGroup, 0)
        mainHBox.addLayout(self._btnHBox, 0)
        mainWidget = QWidget()
        mainWidget.setLayout(mainHBox)
        self.setWidget(mainWidget)

    def _clearFilters(self):
        self._platforms.clearSelection()
        self._regions.clearSelection()
        self._genres.clearSelection()
        self._item.setCheckState(Qt.PartiallyChecked)
        self._box.setCheckState(Qt.PartiallyChecked)
        self._manual.setCheckState(Qt.PartiallyChecked)

    def getSelections(self):
        self._selections = defaultdict(set)  # Reset selections
        if len(self._platforms.selectedItems()) > 0:
            platforms = [x.text() for x in self._platforms.selectedItems()]
            for platform in platforms:
                self._selections["Platform"].add(platform)
        if len(self._regions.selectedItems()) > 0:
            regions = [x.text() for x in self._regions.selectedItems()]
            for region in regions:
                self._selections["Region"].add(region)
        if len(self._genres.selectedItems()) > 0:
            genres = [x.text() for x in self._genres.selectedItems()]
            for genre in genres:
                self._selections["Genre"].add(genre)
        if len(self._years.selectedItems()) > 0:
            years = [x.text() for x in self._years.selectedItems()]
            for year in years:
                self._selections["Year"].add(year)
        if self._item.checkState() is not Qt.PartiallyChecked:
            self._selections[self._item.text()].add("Yes" if self._item.isChecked() else "No")
        if self._manual.checkState() is not Qt.PartiallyChecked:
            self._selections["Manual"].add("Yes" if self._manual.isChecked() else "No")
        if self._box.checkState() is not Qt.PartiallyChecked:
            self._selections["Box"].add("Yes" if self._box.isChecked() else "No")

        return self._selections

    def setItemType(self, itemType: int):
        if 0 < itemType < 4:
            if self._item.text() in self._selections:
                # Delete previous item entry so we don't search for the wrong type in the wrong table
                del self._selections[self._item.text()]
            self._item.setText(self._itemType[itemType])

    def toggleVisibility(self):
        self.setVisible(False if self.isVisible() else True)

    def updatePlatforms(self, platforms):
        self._platforms.clear()
        self._platforms.addItems(platforms)

    def updateRegions(self, regions):
        self._regions.clear()
        self._regions.addItems(regions)

    def updateGenres(self, genres):
        self._genres.clear()
        self._genres.addItems(genres)

    def updateYears(self, years):
        self._years.clear()
        self._years.addItems(years)