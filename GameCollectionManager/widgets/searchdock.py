from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDockWidget, QWidget, QComboBox, QListWidget, QHBoxLayout, QLabel, QPushButton, \
    QAbstractItemView, QVBoxLayout


class AdvancedSearch(QDockWidget):
    def __init__(self, platforms):
        super(AdvancedSearch, self).__init__()

        self.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetClosable)
        self.setFixedHeight(150)
        self.setVisible(True)
        self.setWindowTitle("Advanced search options")

        self.platformsLabel = QLabel("Platforms")
        self.platforms = QListWidget()
        self.platforms.addItems(platforms)
        self.platforms.setSelectionMode(QAbstractItemView.MultiSelection)
        self.platforms.setMaximumWidth(200)

        self.regionLabel = QLabel("Region")
        self.region = QListWidget()
        self.region.addItems(["Europe (PAL)", "Japan", "North America"])
        self.region.setSelectionMode(QAbstractItemView.MultiSelection)
        self.region.setMaximumWidth(200)

        self.labelHBox = QHBoxLayout()
        self.labelHBox.addWidget(self.platformsLabel, 0)
        self.labelHBox.addWidget(self.regionLabel, 1)

        self.selectionHBox = QHBoxLayout()
        self.selectionHBox.setAlignment(Qt.AlignLeft)
        self.selectionHBox.addWidget(self.platforms, 0, 0)
        self.selectionHBox.addWidget(self.region, 1, 0)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.labelHBox, 0)
        self.vbox.addLayout(self.selectionHBox, 1)

        newWidget = QWidget()
        newWidget.setLayout(self.vbox)
        self.setWidget(newWidget)

    def toggleVisibility(self):
        self.setVisible(False if self.isVisible() else True)
