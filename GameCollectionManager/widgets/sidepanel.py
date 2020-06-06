#!/usr/bin/env python
from os import path

import requests
from PySide2.QtCore import Signal
from PySide2.QtGui import Qt, QPixmap, QFont
from PySide2.QtWidgets import QDockWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFrame, QLineEdit, \
    QTextEdit, QStackedLayout, QCheckBox, QComboBox

from utilities.fetchinfo import getMobyRelease


class SidePanel(QDockWidget):
    saved = Signal(dict)

    def __init__(self):
        super(SidePanel, self).__init__()

        # Internal variables
        self._coverdir = path.join("data", "images", "covers")
        self._id = ""
        self._imagedata = ""
        size = [220, 16]  # Width, Height (for QLineEdits/QTextEdits)

        # QDockWidget settings
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetClosable)
        self.setFixedWidth(350)
        self.setVisible(False)

        # Fonts
        bold = QFont()
        bold.setBold(True)
        boldUnderline = QFont()
        boldUnderline.setBold(True)
        boldUnderline.setUnderline(True)

        # Horizontal line
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)

        """Widgets"""
        # Cover
        self.cover = QLabel()
        self.cover.setAlignment(Qt.AlignCenter)
        self.cover.setMinimumHeight(200)
        self.cover.setMaximumSize(self.width(), 250)
        # Buttons
        self.fetchInfoButton = QPushButton("Fetch missing info")
        self.fetchInfoButton.setToolTip("Try to fetch info from MobyGames")
        self.fetchInfoButton.clicked.connect(self._fetchInfo)
        self.editButton = QPushButton("Edit")
        self.editButton.setCheckable(True)
        self.editButton.clicked.connect(self._edit)
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self._saveInfo)

        # Info layout widgets
        self.detailsInfoLabel = QLabel("Details:")
        self.detailsInfoLabel.setAlignment(Qt.AlignBottom)
        self.detailsInfoLabel.setFont(boldUnderline)
        self.nameInfoLabel = QLabel("Name:")
        self.nameInfoLabel.setFont(bold)
        self.nameDataLabel = QLabel()
        self.nameDataLabel.setWordWrap(True)
        self.platformInfoLabel = QLabel("Platform:")
        self.platformInfoLabel.setFont(bold)
        self.platformDataLabel = QLabel()
        self.publisherInfoLabel = QLabel("Publisher:")
        self.publisherInfoLabel.setFont(bold)
        self.publisherDataLabel = QLabel()
        self.developerInfoLabel = QLabel("Developer:")
        self.developerInfoLabel.setFont(bold)
        self.developerDataLabel = QLabel()
        self.regionInfoLabel = QLabel("Region:")
        self.regionInfoLabel.setFont(bold)
        self.regionDataLabel = QLabel()
        self.codeInfoLabel = QLabel("Code:")
        self.codeInfoLabel.setFont(bold)
        self.codeDataLabel = QLabel()
        self.codeDataLabel.setWordWrap(True)
        self.itemInfoLabel = QLabel("Game:")
        self.itemInfoLabel.setFont(bold)
        self.itemDataLabel = QLabel()
        self.boxInfoLabel = QLabel("Box:")
        self.boxInfoLabel.setFont(bold)
        self.boxDataLabel = QLabel()
        self.manualInfoLabel = QLabel("Manual:")
        self.manualInfoLabel.setFont(bold)
        self.manualDataLabel = QLabel()
        self.genreInfoLabel = QLabel("Genre:")
        self.genreInfoLabel.setFont(bold)
        self.genreDataLabel = QLabel()
        self.yearInfoLabel = QLabel("Year:")
        self.yearInfoLabel.setFont(bold)
        self.yearDataLabel = QLabel()
        self.commentInfoLabel = QLabel("Comment:")
        self.commentInfoLabel.setFont(bold)
        self.commentDataLabel = QLabel()
        self.commentDataLabel.setWordWrap(True)
        self.platformsInfoLabel = QLabel("Available for:")
        self.platformsInfoLabel.setFont(bold)
        self.platformsDataLabel = QLabel()
        self.platformsDataLabel.setWordWrap(True)
        self.platformsDataLabel.setMaximumHeight(50)  # Can get quite large otherwise

        # Edit layout widgets
        self.detailsEditLabel = QLabel("Details:")
        self.detailsEditLabel.setAlignment(Qt.AlignBottom)
        self.detailsEditLabel.setFont(boldUnderline)
        self.nameEditLabel = QLabel("Name:")
        self.nameEditLabel.setFont(bold)
        self.nameDataTE = QTextEdit()
        self.nameDataTE.setMaximumSize(size[0], size[1] * 2)
        self.platformEditLabel = QLabel("Platform:")
        self.platformEditLabel.setFont(bold)
        self.platformDataLE = QLineEdit()
        self.platformDataLE.setMaximumSize(size[0], size[1])
        self.publisherEditLabel = QLabel("Publisher:")
        self.publisherEditLabel.setFont(bold)
        self.publisherDataLE = QLineEdit()
        self.publisherDataLE.setMaximumSize(size[0], size[1])
        self.developerEditLabel = QLabel("Developer:")
        self.developerEditLabel.setFont(bold)
        self.developerDataLE = QLineEdit()
        self.developerDataLE.setMaximumSize(size[0], size[1])
        self.regionEditLabel = QLabel("Region:")
        self.regionEditLabel.setFont(bold)
        self.regionDataCoB = QComboBox()
        self.regionDataCoB.addItems(("NTSC (JP)", "NTSC (NA)", "PAL"))
        self.regionDataCoB.setMinimumWidth(size[0])  # If not set it will be too small
        self.regionDataCoB.setMaximumSize(size[0], size[1])
        self.codeEditLabel = QLabel("Code:")
        self.codeEditLabel.setFont(bold)
        self.codeDataLE = QLineEdit()
        self.codeDataLE.setMaximumSize(size[0], size[1])
        self.itemEditLabel = QLabel("Game:")
        self.itemEditLabel.setFont(bold)
        self.itemDataCB = QCheckBox()
        self.itemDataCB.setChecked(False)
        self.boxEditLabel = QLabel("Box:")
        self.boxEditLabel.setFont(bold)
        self.boxDataCB = QCheckBox()
        self.boxDataCB.setChecked(False)
        self.manualEditLabel = QLabel("Manual:")
        self.manualEditLabel.setFont(bold)
        self.manualDataCB = QCheckBox()
        self.manualDataCB.setChecked(False)
        self.genreEditLabel = QLabel("Genre:")
        self.genreEditLabel.setFont(bold)
        self.genreDataLE = QLineEdit()
        self.genreDataLE.setMaximumSize(size[0], size[1])
        self.yearEditLabel = QLabel("Year:")
        self.yearEditLabel.setFont(bold)
        self.yearDataLE = QLineEdit()
        self.yearDataLE.setMaximumSize(size[0], size[1])
        self.commentEditLabel = QLabel("Comment:")
        self.commentEditLabel.setFont(bold)
        self.commentDataTE = QTextEdit()
        self.commentDataTE.setMaximumSize(size[0], size[1] * 2)
        self.platformsEditLabel = QLabel("Available for:")
        self.platformsEditLabel.setFont(bold)
        self.platformsDataTE = QTextEdit()
        self.platformsDataTE.setMaximumSize(size[0], size[1] * 2)

        """Layouts"""
        # Cover
        self.coverVbox = QVBoxLayout()
        self.coverVbox.addWidget(self.cover, 1)
        self.coverVbox.addWidget(hline, 0)

        # Button
        self.buttonHbox = QHBoxLayout()
        self.buttonHbox.addWidget(self.fetchInfoButton, 0)
        self.buttonHbox.addWidget(self.editButton, 0)
        self.buttonHbox.addWidget(self.saveButton, 0)

        # Info layouts
        self.detailsInfoHbox = QHBoxLayout()
        self.detailsInfoHbox.addWidget(self.detailsInfoLabel, 0)
        self.nameInfoHbox = QHBoxLayout()
        self.nameInfoHbox.addWidget(self.nameInfoLabel, 0)
        self.nameInfoHbox.addWidget(self.nameDataLabel, 0)
        self.platformInfoHbox = QHBoxLayout()
        self.platformInfoHbox.addWidget(self.platformInfoLabel, 0)
        self.platformInfoHbox.addWidget(self.platformDataLabel, 0)
        self.publisherInfoHbox = QHBoxLayout()
        self.publisherInfoHbox.addWidget(self.publisherInfoLabel, 0)
        self.publisherInfoHbox.addWidget(self.publisherDataLabel, 0)
        self.developerInfoHbox = QHBoxLayout()
        self.developerInfoHbox.addWidget(self.developerInfoLabel, 0)
        self.developerInfoHbox.addWidget(self.developerDataLabel, 0)
        self.regionInfoHbox = QHBoxLayout()
        self.regionInfoHbox.addWidget(self.regionInfoLabel, 0)
        self.regionInfoHbox.addWidget(self.regionDataLabel, 0)
        self.codeInfoHbox = QHBoxLayout()
        self.codeInfoHbox.addWidget(self.codeInfoLabel, 0)
        self.codeInfoHbox.addWidget(self.codeDataLabel, 0)
        self.itemInfoHbox = QHBoxLayout()
        self.itemInfoHbox.addWidget(self.itemInfoLabel, 0)
        self.itemInfoHbox.addWidget(self.itemDataLabel, 0)
        self.boxInfoHbox = QHBoxLayout()
        self.boxInfoHbox.addWidget(self.boxInfoLabel, 0)
        self.boxInfoHbox.addWidget(self.boxDataLabel, 0)
        self.manualInfoHbox = QHBoxLayout()
        self.manualInfoHbox.addWidget(self.manualInfoLabel, 0)
        self.manualInfoHbox.addWidget(self.manualDataLabel, 0)
        self.genreInfoHbox = QHBoxLayout()
        self.genreInfoHbox.addWidget(self.genreInfoLabel, 0)
        self.genreInfoHbox.addWidget(self.genreDataLabel, 0)
        self.yearInfoHbox = QHBoxLayout()
        self.yearInfoHbox.addWidget(self.yearInfoLabel, 0)
        self.yearInfoHbox.addWidget(self.yearDataLabel, 0)
        self.commentInfoHbox = QHBoxLayout()
        self.commentInfoHbox.addWidget(self.commentInfoLabel, 0)
        self.commentInfoHbox.addWidget(self.commentDataLabel, 0)
        self.platformsInfoHbox = QHBoxLayout()
        self.platformsInfoHbox.addWidget(self.platformsInfoLabel, 0)
        self.platformsInfoHbox.addWidget(self.platformsDataLabel, 0)

        # Edit layouts
        self.detailsEditHbox = QHBoxLayout()
        self.detailsEditHbox.addWidget(self.detailsEditLabel, 0)
        self.nameEditHbox = QHBoxLayout()
        self.nameEditHbox.addWidget(self.nameEditLabel, 0)
        self.nameEditHbox.addWidget(self.nameDataTE, 0)
        self.platformEditHbox = QHBoxLayout()
        self.platformEditHbox.addWidget(self.platformEditLabel, 0)
        self.platformEditHbox.addWidget(self.platformDataLE, 0)
        self.publisherEditHbox = QHBoxLayout()
        self.publisherEditHbox.addWidget(self.publisherEditLabel, 0)
        self.publisherEditHbox.addWidget(self.publisherDataLE, 0)
        self.developerEditHbox = QHBoxLayout()
        self.developerEditHbox.addWidget(self.developerEditLabel, 0)
        self.developerEditHbox.addWidget(self.developerDataLE, 0)
        self.regionEditHbox = QHBoxLayout()
        self.regionEditHbox.addWidget(self.regionEditLabel, 0)
        self.regionEditHbox.addWidget(self.regionDataCoB, 0)
        self.codeEditHbox = QHBoxLayout()
        self.codeEditHbox.addWidget(self.codeEditLabel, 0)
        self.codeEditHbox.addWidget(self.codeDataLE, 0)
        self.itemEditHbox = QHBoxLayout()
        self.itemEditHbox.addWidget(self.itemEditLabel, 0)
        self.itemEditHbox.addWidget(self.itemDataCB, 0)  # TODO: This, and the other checkboxes, doesn't align well.
        self.boxEditHbox = QHBoxLayout()
        self.boxEditHbox.addWidget(self.boxEditLabel, 0)
        self.boxEditHbox.addWidget(self.boxDataCB, 0)
        self.manualEditHbox = QHBoxLayout()
        self.manualEditHbox.addWidget(self.manualEditLabel, 0)
        self.manualEditHbox.addWidget(self.manualDataCB, 0)
        self.genreEditHbox = QHBoxLayout()
        self.genreEditHbox.addWidget(self.genreEditLabel, 0)
        self.genreEditHbox.addWidget(self.genreDataLE, 0)
        self.yearEditHbox = QHBoxLayout()
        self.yearEditHbox.addWidget(self.yearEditLabel, 0)
        self.yearEditHbox.addWidget(self.yearDataLE, 0)
        self.commentEditHbox = QHBoxLayout()
        self.commentEditHbox.addWidget(self.commentEditLabel, 0)
        self.commentEditHbox.addWidget(self.commentDataTE, 0)
        self.platformsEditHbox = QHBoxLayout()
        self.platformsEditHbox.addWidget(self.platformsEditLabel, 0)
        self.platformsEditHbox.addWidget(self.platformsDataTE, 0)

        # Info layout
        self.infoLayout = QVBoxLayout()
        self.infoLayout.addLayout(self.detailsInfoHbox, 0)
        self.infoLayout.addLayout(self.nameInfoHbox, 0)
        self.infoLayout.addLayout(self.platformInfoHbox, 0)
        self.infoLayout.addLayout(self.publisherInfoHbox, 0)
        self.infoLayout.addLayout(self.developerInfoHbox, 0)
        self.infoLayout.addLayout(self.genreInfoHbox, 0)
        self.infoLayout.addLayout(self.regionInfoHbox, 0)
        self.infoLayout.addLayout(self.yearInfoHbox, 0)
        self.infoLayout.addLayout(self.codeInfoHbox, 0)
        self.infoLayout.addLayout(self.itemInfoHbox, 0)
        self.infoLayout.addLayout(self.boxInfoHbox, 0)
        self.infoLayout.addLayout(self.manualInfoHbox, 0)
        self.infoLayout.addLayout(self.commentInfoHbox, 0)
        self.infoLayout.addLayout(self.platformsInfoHbox, 0)

        # Edit layout
        self.editLayout = QVBoxLayout()
        self.editLayout.addLayout(self.detailsEditHbox, 0)
        self.editLayout.addLayout(self.nameEditHbox, 0)
        self.editLayout.addLayout(self.platformEditHbox, 0)
        self.editLayout.addLayout(self.publisherEditHbox, 0)
        self.editLayout.addLayout(self.developerEditHbox, 0)
        self.editLayout.addLayout(self.genreEditHbox, 0)
        self.editLayout.addLayout(self.regionEditHbox, 0)
        self.editLayout.addLayout(self.yearEditHbox, 0)
        self.editLayout.addLayout(self.codeEditHbox, 0)
        self.editLayout.addLayout(self.itemEditHbox, 0)
        self.editLayout.addLayout(self.boxEditHbox, 0)
        self.editLayout.addLayout(self.manualEditHbox, 0)
        self.editLayout.addLayout(self.commentEditHbox, 0)
        self.editLayout.addLayout(self.platformsEditHbox, 0)

        """Main layout"""
        self.infoWidget = QWidget()
        self.infoWidget.setLayout(self.infoLayout)
        self.editWidget = QWidget()
        self.editWidget.setLayout(self.editLayout)
        # Add info and edit widgets to a stacked layout so we can switch layouts when editing
        self.stackedLayout = QStackedLayout()
        self.stackedLayout.addWidget(self.infoWidget)
        self.stackedLayout.addWidget(self.editWidget)
        self.stackedLayout.setCurrentIndex(0)  # Default to info layout

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.coverVbox, 1)
        self.mainLayout.addLayout(self.stackedLayout, 0)
        self.mainLayout.addLayout(self.buttonHbox, 0)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)

    def _edit(self):
        if self.editButton.isChecked():
            self._updateWidgetData(1)
            self.stackedLayout.setCurrentIndex(1)
        else:
            self._updateWidgetData(0)
            self.stackedLayout.setCurrentIndex(0)

    def _fetchInfo(self):
        name = self.nameDataLabel.text()
        platform = self.platformDataLabel.text()
        region = self.regionDataLabel.text()
        info = getMobyRelease(name, platform, region)
        if "image" in info.keys() and info["image"] != "":
            self._imagedata = requests.get(info["image"]).content
            pixmap = QPixmap()
            pixmap.loadFromData(self._imagedata)
            w = self.cover.width()
            h = self.cover.height()
            self.cover.setPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        if self.publisherDataLabel.text() == "":
            self.publisherDataLabel.setText(info["publisher"])
        if self.developerDataLabel.text() == "":
            self.developerDataLabel.setText(info["developer"])
        if self.genreDataLabel.text() == "":
            self.genreDataLabel.setText(info["genre"])
        if self.yearDataLabel.text() == "":
            self.yearDataLabel.setText(info["year"])
        if self.codeDataLabel.text() == "":
            self.codeDataLabel.setText(info["code"])
        if self.platformsDataLabel.text() == "":
            self.platformsDataLabel.setText(info["platforms"])
        # Update edit widgets if we're editing:
        if self.editButton.isChecked():
            self._updateWidgetData(1)

    def _saveInfo(self):
        if self.editButton.isChecked():
            self._updateWidgetData(0)

        info = {"Name": self.nameDataLabel.text(),
                "Platform": self.platformDataLabel.text(),
                "Publisher": self.publisherDataLabel.text(),
                "Developer": self.developerDataLabel.text(),
                "Genre": self.genreDataLabel.text(),
                "Region": self.regionDataLabel.text(),
                "Year": self.yearDataLabel.text(),
                "Code": self.codeDataLabel.text(),
                "Item": self.itemDataLabel.text(),
                "Box": self.boxDataLabel.text(),
                "Manual": self.manualDataLabel.text(),
                "Comment": self.commentDataLabel.text(),
                "Platforms": self.platformsDataLabel.text()}

        # Save imagedata to file
        if self._imagedata != "" and not path.exists(path.join(self._coverdir, self._id)):
            with open(path.join(self._coverdir, self._id), "wb") as f:
                f.write(self._imagedata)

        self.saved.emit(info)

    def _updateWidgetData(self, layoutIndex: int):
        if layoutIndex == 0:
            self.nameDataLabel.setText(self.nameDataTE.toPlainText())
            self.platformDataLabel.setText(self.platformDataLE.text())
            self.publisherDataLabel.setText(self.publisherDataLE.text())
            self.developerDataLabel.setText(self.developerDataLE.text())
            self.genreDataLabel.setText(self.genreDataLE.text())
            self.regionDataLabel.setText(self.regionDataCoB.currentText())
            self.yearDataLabel.setText(self.yearDataLE.text())
            self.codeDataLabel.setText(self.codeDataLE.text())
            self.itemDataLabel.setText("Yes") if self.itemDataCB.isChecked() else self.itemDataLabel.setText("No")
            self.boxDataLabel.setText("Yes") if self.boxDataCB.isChecked() else self.boxDataLabel.setText("No")
            self.manualDataLabel.setText("Yes") if self.manualDataCB.isChecked() else self.manualDataLabel.setText("No")
            self.commentDataLabel.setText(self.commentDataTE.toPlainText())
            self.platformsDataLabel.setText(self.platformsDataTE.toPlainText())
        else:
            self.nameDataTE.setText(self.nameDataLabel.text())
            self.platformDataLE.setText(self.platformDataLabel.text())
            self.publisherDataLE.setText(self.publisherDataLabel.text())
            self.developerDataLE.setText(self.developerDataLabel.text())
            self.genreDataLE.setText(self.genreDataLabel.text())
            self.regionDataCoB.setCurrentIndex(0) if self.regionDataLabel.text == "NTSC (JP)"\
                else self.regionDataCoB.setCurrentIndex(1) if self.regionDataLabel.text == "NTSC (NA)"\
                else self.regionDataCoB.setCurrentIndex(2)
            self.yearDataLE.setText(self.yearDataLabel.text())
            self.codeDataLE.setText(self.codeDataLabel.text())
            self.itemDataCB.setChecked(True) if self.itemDataLabel.text() == "Yes" \
                else self.itemDataCB.setChecked("False")
            self.boxDataCB.setChecked(True) if self.boxDataLabel.text() == "Yes" \
                else self.boxDataCB.setChecked(False)
            self.manualDataCB.setChecked(True) if self.manualDataLabel.text() == "Yes" \
                else self.manualDataCB.setChecked(False)
            self.commentDataTE.setText(self.commentDataLabel.text())
            self.platformsDataTE.setText(self.platformsDataLabel.text())

    def showDetails(self, info: dict):
        if not self.isVisible():
            self.setVisible(True)
        if self.editButton.isChecked():
            self.editButton.setChecked(False)
        self.stackedLayout.setCurrentIndex(0)  # Show info layout initially

        self._id = str(info["ID"]) + ".jpg"
        self._imagedata = ""
        pixmap = path.join(self._coverdir, "none.png")
        if path.exists(path.join(self._coverdir, self._id)) and info["Table"] == "games":
            pixmap = path.join(self._coverdir, self._id)
        p = QPixmap(pixmap)
        w = self.cover.width()
        h = self.cover.height()
        self.cover.setPixmap(p.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.nameDataLabel.setText(info["Name"])
        self.platformDataLabel.setText(info["Platform"])
        self.regionDataLabel.setText(info["Region"])
        self.boxDataLabel.setText(info["Box"])
        self.manualDataLabel.setText(info["Manual"])
        self.yearDataLabel.setText(str(info["Year"]))
        self.commentDataLabel.setText(info["Comment"])
        if info["Table"] == "games":
            self.publisherDataLabel.setText(info["Publisher"])
            self.developerDataLabel.setText(info["Developer"])
            self.genreInfoLabel.setText("Genre:")
            self.genreEditLabel.setText("Genre:")
            self.genreDataLabel.setText(info["Genre"])
            self.codeInfoLabel.setText("Code:")
            self.codeInfoLabel.setVisible(True)
            self.codeEditLabel.setText("Code")
            self.codeEditLabel.setVisible(True)
            self.codeDataLabel.setText(info["Code"])
            self.codeDataLabel.setVisible(True)
            self.codeDataLE.setVisible(True)
            self.itemInfoLabel.setText("Game:")
            self.itemEditLabel.setText("Game:")
            self.itemDataLabel.setText(info["Game"])
            self.platformsDataLabel.setText(info["Platforms"])
            self.platformsDataLabel.setVisible(True)
            self.platformsInfoLabel.setVisible(True)
            self.fetchInfoButton.setEnabled(True)
            self.fetchInfoButton.setVisible(True)
            self.fetchInfoButton.setToolTip("Try to fetch info from MobyGames")
            self.saveButton.setEnabled(True)
            self.saveButton.setVisible(True)
        elif info["Table"] == "consoles":
            self.genreInfoLabel.setText("Country:")
            self.genreEditLabel.setText("Country:")
            self.genreDataLabel.setText(info["Country"])
            self.codeInfoLabel.setText("Serial Number:")
            self.codeInfoLabel.setVisible(True)
            self.codeEditLabel.setText("Serial Number:")
            self.codeEditLabel.setVisible(True)
            self.codeDataLabel.setText(info["Serial number"])
            self.codeDataLabel.setVisible(True)
            self.codeDataLE.setVisible(True)
            self.itemInfoLabel.setText("Console:")
            self.itemEditLabel.setText("Console:")
            self.itemDataLabel.setText(info["Console"])
            self.platformsInfoLabel.setVisible(False)
            self.platformsDataLabel.setVisible(False)
            self.fetchInfoButton.setEnabled(False)
            self.fetchInfoButton.setToolTip("Not available for Consoles tab")
        elif info["Table"] == "accessories":
            self.genreInfoLabel.setText("Country:")
            self.genreEditLabel.setText("Country:")
            self.genreDataLabel.setText(info["Country"])
            self.itemInfoLabel.setText("Accessory:")
            self.itemEditLabel.setText("Accessory:")
            self.itemDataLabel.setText(info["Accessory"])
            self.codeInfoLabel.setVisible(False)
            self.codeEditLabel.setVisible(False)
            self.codeDataLabel.setVisible(False)
            self.codeDataLE.setVisible(False)
            self.platformsInfoLabel.setVisible(False)
            self.platformsDataLabel.setVisible(False)
            self.fetchInfoButton.setEnabled(False)
            self.fetchInfoButton.setToolTip("Not avaiable for Accessories tab")

    def hideDetails(self):
        self.setVisible(False)
