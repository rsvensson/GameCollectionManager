from collections.__init__ import OrderedDict

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QDialog, QLabel, QComboBox, QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, \
    QInputDialog, QDesktopWidget, QMessageBox


class InputWindow(QDialog):
    """Window where user can enter new data into a table.
       It returns the data formatted into an OrderedDict.
       platforms: the platforms from the currently loaded
                  collection."""

    def __init__(self, platforms, parent=None):
        super(InputWindow, self).__init__(parent=parent)

        self.setContentsMargins(5, 5, 5, 5)

        self.dataTypes = ["Game", "Console", "Accessory"]
        self.dataTypeLabel = QLabel("Type\t ")
        self.dataType = QComboBox()
        self.dataType.addItems(self.dataTypes)
        self.dataType.currentIndexChanged.connect(self._changeWidgets)

        self.nameLabel = QLabel("Name\t ")
        self.name = QLineEdit()

        self.platformLabel = QLabel("Platform\t ")
        self.platform = QComboBox()
        self.platform.addItems(platforms if len(platforms) > 0 else " ")
        self.platform.addItem("(New platform)")
        self.platform.currentIndexChanged.connect(self._addPlatform)

        self.regionLabel = QLabel("Region\t ")
        self.region = QLineEdit()

        self.countryLabel = QLabel("Country\t ")
        self.country = QLineEdit()
        self.country.setEnabled(False)

        self.codeLabel = QLabel("Code\t ")
        self.code = QLineEdit()

        self.itemLabel = QLabel("Game")
        self.item = QCheckBox()

        self.boxLabel = QLabel("Box")
        self.box = QCheckBox()

        self.manualLabel = QLabel("Manual")
        self.manual = QCheckBox()

        self.yearLabel = QLabel("Year\t ")
        self.year = QLineEdit()

        self.commentLabel = QLabel("Comment")
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
        self.hboxCountry = QHBoxLayout()
        self.hboxCountry.addStretch()
        self.hboxBoxMan = QHBoxLayout()
        self.hboxYear = QHBoxLayout()
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
        self.hboxCountry.addWidget(self.countryLabel, 0)
        self.hboxCountry.addWidget(self.country, 1)
        self.hboxYear.addWidget(self.yearLabel, 0)
        self.hboxYear.addWidget(self.year, 1)
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
        self.hboxBtn.addWidget(self.okButton, 0)
        self.hboxBtn.addWidget(self.cnclButton, 1)

        self.vbox.addLayout(self.hboxType, 0)
        self.vbox.addLayout(self.hboxName, 1)
        self.vbox.addLayout(self.hboxPlatform, 2)
        self.vbox.addLayout(self.hboxRegion, 3)
        self.vbox.addLayout(self.hboxCode, 4)
        self.vbox.addLayout(self.hboxCountry, 5)
        self.vbox.addLayout(self.hboxYear, 6)
        self.vbox.addLayout(self.hboxComment, 7)
        self.vbox.addLayout(self.hboxBoxMan, 8)
        self.vbox.addLayout(self.hboxBtn, 9)

        self.setLayout(self.vbox)

        self.setWindowTitle("Add to collection")
        self.setFixedSize(QSize(500, 280))
        self._center()

    def _addPlatform(self):
        if self.platform.currentText() == "(New platform)":
            while True:
                platform, ok = QInputDialog.getText(self, "Add platform",
                                                "Platform name:")
                if ok:
                    if platform == "" or platform.isspace():
                        msgBox = QMessageBox()
                        msgBox.setIcon(QMessageBox.Warning)
                        msgBox.setWindowTitle("Invalid platform")
                        msgBox.setText("<h2>Invalid platform</h2>")
                        msgBox.setInformativeText("Can't add empty string or whitespace.")
                        msgBox.exec_()
                    else:
                        lastIndex = self.platform.count()
                        self.platform.addItem(platform)
                        self.platform.setCurrentIndex(lastIndex)
                        self.platform.removeItem(self.platform.findText(" "))  # Remove the temp empty item if any
                        break
                else:
                    break


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
                                ('Year', '{}'.format(self.year.text())),
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
                                ('Year', '{}'.format(self.year.text())),
                                ('Comment', '{}'.format(self.comment.text()))])

        elif self.dataType.currentIndex() == 2:
            data = OrderedDict([('Platform', '{}'.format(self.platform.currentText())),
                                ('Name', '{}'.format(self.name.text())),
                                ('Region', '{}'.format(self.region.text())),
                                ('Country', '{}'.format(self.country.text())),
                                ('Accessory', '{}'.format('Yes' if self.item.isChecked() else 'No')),
                                ('Box', '{}'.format('Yes' if self.box.isChecked() else 'No')),
                                ('Manual', '{}'.format('Yes' if self.manual.isChecked() else 'No')),
                                ('Year', '{}'.format(self.year.text())),
                                ('Comment', '{}'.format(self.comment.text()))])

        return data
