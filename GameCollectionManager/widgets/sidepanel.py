#!/usr/bin/env python
from PySide2.QtCore import Signal
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QDockWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton

from utilities.fetchinfo import getMobyRelease


class SidePanel(QDockWidget):
    saved = Signal(dict)

    def __init__(self):
        super(SidePanel, self).__init__()

        # QDockWidget settings
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetClosable)
        self.setFixedWidth(350)
        self.setVisible(False)
        self.setWindowTitle("Details")

        # Labels
        self.nameLabel = QLabel("Name")
        self.nameInfoLabel = QLabel()
        self.platformLabel = QLabel("Platform")
        self.platformInfoLabel = QLabel()
        self.publisherLabel = QLabel("Publisher")
        self.publisherInfoLabel = QLabel()
        self.developerLabel = QLabel("Developer")
        self.developerInfoLabel = QLabel()
        self.platformsLabel = QLabel("Available for")
        self.platformsInfoLabel = QLabel()
        self.platformsInfoLabel.setWordWrap(True)
        self.regionLabel = QLabel("Region")
        self.regionInfoLabel = QLabel()
        self.codeLabel = QLabel("Code")
        self.codeInfoLabel = QLabel()
        self.itemLabel = QLabel("Game")
        self.itemInfoLabel = QLabel()
        self.boxLabel = QLabel("Box")
        self.boxInfoLabel = QLabel()
        self.manualLabel = QLabel("Manual")
        self.manualInfoLabel = QLabel()
        self.genreLabel = QLabel("Genre")
        self.genreInfoLabel = QLabel()
        self.yearLabel = QLabel("Year")
        self.yearInfoLabel = QLabel()
        self.commentLabel = QLabel("Comment")
        self.commentInfoLabel = QLabel()
        self.commentInfoLabel.setWordWrap(True)

        # Buttons
        self.fetchInfoButton = QPushButton("Fetch missing info")
        self.fetchInfoButton.clicked.connect(self._fetchInfo)
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self._saveInfo)

        # Layouts
        self.nameHbox = QHBoxLayout()
        self.nameHbox.addWidget(self.nameLabel, 0)
        self.nameHbox.addWidget(self.nameInfoLabel, 0)
        self.platformHbox = QHBoxLayout()
        self.platformHbox.addWidget(self.platformLabel, 0)
        self.platformHbox.addWidget(self.platformInfoLabel, 0)
        self.publisherHbox = QHBoxLayout()
        self.publisherHbox.addWidget(self.publisherLabel, 0)
        self.publisherHbox.addWidget(self.publisherInfoLabel, 0)
        self.developerHbox = QHBoxLayout()
        self.developerHbox.addWidget(self.developerLabel, 0)
        self.developerHbox.addWidget(self.developerInfoLabel, 0)
        self.platformsHbox = QHBoxLayout()
        self.platformsHbox.addWidget(self.platformsLabel, 0)
        self.platformsHbox.addWidget(self.platformsInfoLabel, 0)
        self.regionHbox = QHBoxLayout()
        self.regionHbox.addWidget(self.regionLabel, 0)
        self.regionHbox.addWidget(self.regionInfoLabel, 0)
        self.codeHbox = QHBoxLayout()
        self.codeHbox.addWidget(self.codeLabel, 0)
        self.codeHbox.addWidget(self.codeInfoLabel, 0)
        self.itemHbox = QHBoxLayout()
        self.itemHbox.addWidget(self.itemLabel, 0)
        self.itemHbox.addWidget(self.itemInfoLabel, 0)
        self.boxHbox = QHBoxLayout()
        self.boxHbox.addWidget(self.boxLabel, 0)
        self.boxHbox.addWidget(self.boxInfoLabel, 0)
        self.manualHbox = QHBoxLayout()
        self.manualHbox.addWidget(self.manualLabel, 0)
        self.manualHbox.addWidget(self.manualInfoLabel, 0)
        self.genreHbox = QHBoxLayout()
        self.genreHbox.addWidget(self.genreLabel, 0)
        self.genreHbox.addWidget(self.genreInfoLabel, 0)
        self.yearHbox = QHBoxLayout()
        self.yearHbox.addWidget(self.yearLabel, 0)
        self.yearHbox.addWidget(self.yearInfoLabel, 0)
        self.commentHbox = QHBoxLayout()
        self.commentHbox.addWidget(self.commentLabel, 0)
        self.commentHbox.addWidget(self.commentInfoLabel, 0)
        self.buttonHbox = QHBoxLayout()
        self.buttonHbox.addWidget(self.fetchInfoButton, 0)
        self.buttonHbox.addWidget(self.saveButton, 0)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.nameHbox, 0)
        self.mainLayout.addLayout(self.platformHbox, 0)
        self.mainLayout.addLayout(self.publisherHbox, 0)
        self.mainLayout.addLayout(self.developerHbox, 0)
        self.mainLayout.addLayout(self.genreHbox, 0)
        self.mainLayout.addLayout(self.regionHbox, 0)
        self.mainLayout.addLayout(self.yearHbox, 0)
        self.mainLayout.addLayout(self.codeHbox, 0)
        self.mainLayout.addLayout(self.itemHbox, 0)
        self.mainLayout.addLayout(self.boxHbox, 0)
        self.mainLayout.addLayout(self.manualHbox, 0)
        self.mainLayout.addLayout(self.commentHbox, 0)
        self.mainLayout.addLayout(self.platformsHbox, 0)
        self.mainLayout.addLayout(self.buttonHbox, 0)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)

    def _fetchInfo(self):
        name = self.nameInfoLabel.text()
        platform = self.platformInfoLabel.text()
        region = self.regionInfoLabel.text()
        info = getMobyRelease(name, platform, region)

        if self.publisherInfoLabel.text() == "":
            self.publisherInfoLabel.setText(info["publisher"])
        if self.developerInfoLabel.text() == "":
            self.developerInfoLabel.setText(info["developer"])
        if self.genreInfoLabel.text() == "":
            self.genreInfoLabel.setText(info["genre"])
        if self.yearInfoLabel.text() == "":
            self.yearInfoLabel.setText(info["year"])
        if self.codeInfoLabel.text() == "":
            self.codeInfoLabel.setText(info["code"])
        if self.platformsInfoLabel.text() == "":
            self.platformsInfoLabel.setText(info["platforms"])

    def _saveInfo(self):
        info = {"publisher": self.publisherInfoLabel.text(),
                "developer": self.developerInfoLabel.text(),
                "platforms": self.platformsInfoLabel.text(),
                "genre": self.genreInfoLabel.text(),
                "code": self.codeInfoLabel.text(),
                "year": self.yearInfoLabel.text()}
        self.saved.emit(info)

    def showDetails(self, info):
        if not self.isVisible():
            self.setVisible(True)

        self.nameInfoLabel.setText(info["Name"])
        self.platformInfoLabel.setText(info["Platform"])
        self.publisherInfoLabel.setText(info["Publisher"])
        self.developerInfoLabel.setText(info["Developer"])
        self.genreInfoLabel.setText(info["Genre"])
        self.regionInfoLabel.setText(info["Region"])
        self.yearInfoLabel.setText(str(info["Year"]))
        self.codeInfoLabel.setText(info["Code"])
        self.itemInfoLabel.setText(info["Game"])
        self.boxInfoLabel.setText(info["Box"])
        self.manualInfoLabel.setText(info["Manual"])
        self.commentInfoLabel.setText(info["Comment"])
        self.platformsInfoLabel.setText(info["Platforms"])

    def hideDetails(self):
        self.setVisible(False)
