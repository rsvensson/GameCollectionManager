from collections import defaultdict

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QDockWidget, QWidget, QComboBox, QListWidget, QHBoxLayout, \
    QLabel, QPushButton, QAbstractItemView, QVBoxLayout, QGroupBox


class AdvancedSearch(QDockWidget):
    filterApplied = Signal()

    def __init__(self, platforms, regions):
        super(AdvancedSearch, self).__init__()

        # QDockWidget settings
        self.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetClosable)
        self.setFixedHeight(150)
        self.setVisible(False)
        self.setWindowTitle("Advanced search options")

        # The selected items for each widget are saved in a set-dictionary
        self._selections = defaultdict(set)

        ## Widget settings
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

        # Inventory widgets
        self._itemType = {1: "Game", 2: "Console", 3: "Accessory"}
        self._itemLabel = QLabel(self._itemType[1])
        self._item = QComboBox()
        self._item.addItems(["--", "Yes", "No"])
        self._item.setMaximumSize(self._item.sizeHint())
        self._manualLabel = QLabel("Manual")
        self._manual = QComboBox()
        self._manual.addItems(["--", "Yes", "No"])
        self._manual.setMaximumSize(self._manual.sizeHint())
        self._boxLabel = QLabel("Box")
        self._box = QComboBox()
        self._box.addItems(["--", "Yes", "No"])
        self._box.setMaximumSize(self._box.sizeHint())
        self._inventoryLabelsVBox = QVBoxLayout()
        self._inventoryLabelsVBox.addWidget(self._itemLabel, 0)
        self._inventoryLabelsVBox.addStretch(1)
        self._inventoryLabelsVBox.addWidget(self._boxLabel, 1)
        self._inventoryLabelsVBox.addStretch(1)
        self._inventoryLabelsVBox.addWidget(self._manualLabel, 2)
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
        self._inventoryGroup.setMaximumWidth(150)
        self._inventoryGroup.setLayout(self._haveHBox)

        # Clear and Apply button widgets
        self._clearBtn = QPushButton("Clear selection")
        self._clearBtn.setMaximumSize(self._clearBtn.sizeHint())
        self._clearBtn.clicked.connect(self._clearFilters)
        self._applyBtn = QPushButton("Apply filter")
        self._applyBtn.setMaximumSize(self._clearBtn.sizeHint())
        self._applyBtn.clicked.connect(self._applyFilters)
        self._btnHBox = QHBoxLayout()
        self._btnHBox.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self._btnHBox.addWidget(self._clearBtn, 0)
        self._btnHBox.addWidget(self._applyBtn, 1)

        # General layout
        mainHBox = QHBoxLayout()
        mainHBox.setAlignment(Qt.AlignLeft)
        mainHBox.addLayout(self._platformVBox, 0)
        mainHBox.addLayout(self._regionVBox, 1)
        mainHBox.addWidget(self._inventoryGroup, 2)
        mainHBox.addLayout(self._btnHBox, 3)
        mainWidget = QWidget()
        mainWidget.setLayout(mainHBox)
        self.setWidget(mainWidget)

    def _applyFilters(self):
        self._selections = defaultdict(set)  # Reset state of dictionary
        self.filterApplied.emit()

    def _clearFilters(self):
        self._platforms.clearSelection()
        self._regions.clearSelection()
        self._item.setCurrentIndex(0)
        self._box.setCurrentIndex(0)
        self._manual.setCurrentIndex(0)

    def getSelections(self):
        if len(self._platforms.selectedItems()) > 0:
            temp = [x.text() for x in self._platforms.selectedItems()]
            for platform in temp:
                self._selections["Platform"].add(platform)
        if len(self._regions.selectedItems()) > 0:
            temp = [x.text() for x in self._regions.selectedItems()]
            for region in temp:
                self._selections["Region"].add(region)
        if self._item.currentIndex() != 0:
            self._selections[self._itemLabel.text()].add(self._item.currentText())
        if self._manual.currentIndex() != 0:
            self._selections["Manual"].add(self._manual.currentText())
        if self._box.currentIndex() != 0:
            self._selections["Box"].add(self._box.currentText())

        return self._selections

    def setItemType(self, itemType: int):
        if 0 < itemType < 4:
            if self._itemLabel.text() in self._selections:
                # Delete previous item entry so we don't search for the wrong type in the wrong table
                del self._selections[self._itemLabel.text()]
            self._itemLabel.setText(self._itemType[itemType])

    def toggleVisibility(self):
        self.setVisible(False if self.isVisible() else True)

    def updatePlatforms(self, platforms):
        self._platforms.clear()
        self._platforms.addItems(platforms)

    def updateRegions(self, regions):
        self._regions.clear()
        self._regions.addItems(regions)
