from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QDockWidget, QWidget, QComboBox, QListWidget, QHBoxLayout, QLabel, QPushButton, \
    QAbstractItemView, QVBoxLayout
from collections import defaultdict


class AdvancedSearch(QDockWidget):
    filterApplied = Signal()

    def __init__(self, platforms, regions):
        super(AdvancedSearch, self).__init__()

        self.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetClosable)
        self.setFixedHeight(150)
        self.setVisible(False)
        self.setWindowTitle("Advanced search options")

        self.platformLabel = QLabel("Platform")
        self.platforms = QListWidget()
        self.platforms.addItems(platforms)
        self.platforms.setSelectionMode(QAbstractItemView.MultiSelection)
        self.platforms.setMaximumWidth(200)
        self.platformVBox = QVBoxLayout()
        self.platformVBox.addWidget(self.platformLabel, 0)
        self.platformVBox.addWidget(self.platforms, 1)

        self.regionLabel = QLabel("Region")
        self.regions = QListWidget()
        self.regions.addItems(regions)
        self.regions.setSelectionMode(QAbstractItemView.MultiSelection)
        self.regions.setMaximumWidth(200)
        self.regionVBox = QVBoxLayout()
        self.regionVBox.addWidget(self.regionLabel, 0)
        self.regionVBox.addWidget(self.regions, 1)

        self.clearBtn = QPushButton("Clear selection")
        self.clearBtn.setMaximumSize(self.clearBtn.sizeHint())
        self.clearBtn.clicked.connect(self.clearFilters)
        self.applyBtn = QPushButton("Apply filter")
        self.applyBtn.setMaximumSize(self.clearBtn.sizeHint())
        self.applyBtn.clicked.connect(self.applyFilters)
        self.btnHBox = QHBoxLayout()
        self.btnHBox.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.btnHBox.addWidget(self.clearBtn, 0)
        self.btnHBox.addWidget(self.applyBtn, 1)

        self.hbox = QHBoxLayout()
        self.hbox.setAlignment(Qt.AlignLeft)
        self.hbox.addLayout(self.platformVBox, 0)
        self.hbox.addLayout(self.regionVBox, 1)
        self.hbox.addLayout(self.btnHBox, 2)

        newWidget = QWidget()
        newWidget.setLayout(self.hbox)
        self.setWidget(newWidget)

        self._selections = defaultdict(set)

    def applyFilters(self):
        self._selections = defaultdict(set)  # Reset state of dictionary
        self.filterApplied.emit()

    def clearFilters(self):
        self.platforms.clearSelection()
        self.regions.clearSelection()

    def getSelections(self):
        if len(self.platforms.selectedItems()) > 0:
            temp = [x.text() for x in self.platforms.selectedItems()]
            for platform in temp:
                self._selections["Platform"].add(platform)
        if len(self.regions.selectedItems()) > 0:
            temp = [x.text() for x in self.regions.selectedItems()]
            for region in temp:
                self._selections["Region"].add(region)

        return self._selections

    def toggleVisibility(self):
        self.setVisible(False if self.isVisible() else True)
