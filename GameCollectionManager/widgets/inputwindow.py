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

        self._dataTypes = ["Game", "Console", "Accessory"]
        self._dataTypeLabel = QLabel("Type\t ")
        self._dataType = QComboBox()
        self._dataType.addItems(self._dataTypes)
        self._dataType.currentIndexChanged.connect(self._changeWidgets)

        self._nameLabel = QLabel("Name\t ")
        self._name = QLineEdit()

        self._platformLabel = QLabel("Platform\t ")
        self._platform = QComboBox()
        self._platform.addItems(platforms if len(platforms) > 0 else " ")
        self._platform.addItem("(New platform)")
        self._platform.currentIndexChanged.connect(self._addPlatform)

        self._regionLabel = QLabel("Region\t ")
        self._region = QLineEdit()

        self._countryLabel = QLabel("Country\t ")
        self._countryLabel.setEnabled(False)
        self._country = QLineEdit()
        self._country.setEnabled(False)

        self._codeLabel = QLabel("Code\t ")
        self._code = QLineEdit()

        self._itemLabel = QLabel("Game")
        self._item = QCheckBox()

        self._boxLabel = QLabel("Box")
        self._box = QCheckBox()

        self._manualLabel = QLabel("Manual")
        self._manual = QCheckBox()

        self._yearLabel = QLabel("Year\t ")
        self._year = QLineEdit()

        self._commentLabel = QLabel("Comment")
        self._comment = QLineEdit()

        self._okButton = QPushButton()
        self._okButton.setText("OK")
        self._okButton.setMaximumSize(self._okButton.sizeHint())
        self._okButton.clicked.connect(self.accept)
        self._cnclButton = QPushButton()
        self._cnclButton.setText("Cancel")
        self._cnclButton.setMaximumSize(self._cnclButton.sizeHint())
        self._cnclButton.clicked.connect(self.reject)

        self._vbox = QVBoxLayout()
        self._vbox.addStretch()
        self._hboxType = QHBoxLayout()
        self._hboxType.addStretch()
        self._hboxName = QHBoxLayout()
        self._hboxName.addStretch()
        self._hboxPlatform = QHBoxLayout()
        self._hboxRegion = QHBoxLayout()
        self._hboxRegion.addStretch()
        self._hboxCode = QHBoxLayout()
        self._hboxCode.addStretch()
        self._hboxCountry = QHBoxLayout()
        self._hboxCountry.addStretch()
        self._hboxBoxMan = QHBoxLayout()
        self._hboxYear = QHBoxLayout()
        self._hboxComment = QHBoxLayout()
        self._hboxComment.addStretch()
        self._hboxBtn = QHBoxLayout()
        self._hboxBtn.addStretch()

        self._hboxType.addWidget(self._dataTypeLabel, 0)
        self._hboxType.addWidget(self._dataType, 1)
        self._hboxName.addWidget(self._nameLabel, 0)
        self._hboxName.addWidget(self._name, 1)
        self._hboxPlatform.addWidget(self._platformLabel, 0)
        self._hboxPlatform.addWidget(self._platform, 1)
        self._hboxRegion.addWidget(self._regionLabel, 0)
        self._hboxRegion.addWidget(self._region, 1)
        self._hboxCode.addWidget(self._codeLabel, 0)
        self._hboxCode.addWidget(self._code, 1)
        self._hboxCountry.addWidget(self._countryLabel, 0)
        self._hboxCountry.addWidget(self._country, 1)
        self._hboxYear.addWidget(self._yearLabel, 0)
        self._hboxYear.addWidget(self._year, 1)
        self._hboxComment.addWidget(self._commentLabel, 0)
        self._hboxComment.addWidget(self._comment, 1)
        self._hboxBoxMan.addStretch(10)
        self._hboxBoxMan.addWidget(self._itemLabel, 0)
        self._hboxBoxMan.addWidget(self._item, 1)
        self._hboxBoxMan.addStretch(5)
        self._hboxBoxMan.addWidget(self._boxLabel, 2)
        self._hboxBoxMan.addWidget(self._box, 3)
        self._hboxBoxMan.addStretch(5)
        self._hboxBoxMan.addWidget(self._manualLabel, 4)
        self._hboxBoxMan.addWidget(self._manual, 5)
        self._hboxBoxMan.addStretch(10)
        self._hboxBtn.addWidget(self._okButton, 0)
        self._hboxBtn.addWidget(self._cnclButton, 1)

        self._vbox.addLayout(self._hboxType, 0)
        self._vbox.addLayout(self._hboxName, 1)
        self._vbox.addLayout(self._hboxPlatform, 2)
        self._vbox.addLayout(self._hboxRegion, 3)
        self._vbox.addLayout(self._hboxCode, 4)
        self._vbox.addLayout(self._hboxCountry, 5)
        self._vbox.addLayout(self._hboxYear, 6)
        self._vbox.addLayout(self._hboxComment, 7)
        self._vbox.addLayout(self._hboxBoxMan, 8)
        self._vbox.addLayout(self._hboxBtn, 9)

        self.setLayout(self._vbox)

        self.setWindowTitle("Add to collection")
        self.setFixedSize(QSize(500, 280))
        self._center()

    def _addPlatform(self):
        if self._platform.currentText() == "(New platform)":
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
                        lastIndex = self._platform.count()
                        self._platform.addItem(platform)
                        self._platform.setCurrentIndex(lastIndex)
                        self._platform.removeItem(self._platform.findText(" "))  # Remove the temp empty item if any
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

        if self._dataType.currentIndex() == 0:
            self._codeLabel.setEnabled(True)
            self._code.setEnabled(True)
            self._countryLabel.setEnabled(False)
            self._country.setEnabled(False)
            self._codeLabel.setText("Code\t ")
            self._itemLabel.setText("Game")
        elif self._dataType.currentIndex() == 1:
            self._codeLabel.setEnabled(True)
            self._code.setEnabled(True)
            self._countryLabel.setEnabled(True)
            self._country.setEnabled(True)
            self._codeLabel.setText("Serial No\t ")
            self._itemLabel.setText("Console")
        elif self._dataType.currentIndex() == 2:
            self._countryLabel.setEnabled(True)
            self._country.setEnabled(True)
            self._codeLabel.setEnabled(False)
            self._code.setEnabled(False)
            self._itemLabel.setText("Accessory")

    def returnData(self):
        data = None

        if self._dataType.currentIndex() == 0:
            data = OrderedDict([('Platform', '{}'.format(self._platform.currentText())),
                                ('Name', '{}'.format(self._name.text())),
                                ('Region', '{}'.format(self._region.text())),
                                ('Code', '{}'.format(self._code.text())),
                                ('Game', '{}'.format('Yes' if self._item.isChecked() else 'No')),
                                ('Box', '{}'.format('Yes' if self._box.isChecked() else 'No')),
                                ('Manual', '{}'.format('Yes' if self._manual.isChecked() else 'No')),
                                ('Year', '{}'.format(self._year.text())),
                                ('Comment', '{}'.format(self._comment.text()))])

        elif self._dataType.currentIndex() == 1:
            data = OrderedDict([('Platform', '{}'.format(self._platform.currentText())),
                                ('Name', '{}'.format(self._name.text())),
                                ('Region', '{}'.format(self._region.text())),
                                ('Country', '{}'.format(self._country.text())),
                                ('Serial number', '{}'.format(self._code.text())),
                                ('Console', '{}'.format('Yes' if self._item.isChecked() else 'No')),
                                ('Box', '{}'.format('Yes' if self._box.isChecked() else 'No')),
                                ('Manual', '{}'.format('Yes' if self._manual.isChecked() else 'No')),
                                ('Year', '{}'.format(self._year.text())),
                                ('Comment', '{}'.format(self._comment.text()))])

        elif self._dataType.currentIndex() == 2:
            data = OrderedDict([('Platform', '{}'.format(self._platform.currentText())),
                                ('Name', '{}'.format(self._name.text())),
                                ('Region', '{}'.format(self._region.text())),
                                ('Country', '{}'.format(self._country.text())),
                                ('Accessory', '{}'.format('Yes' if self._item.isChecked() else 'No')),
                                ('Box', '{}'.format('Yes' if self._box.isChecked() else 'No')),
                                ('Manual', '{}'.format('Yes' if self._manual.isChecked() else 'No')),
                                ('Year', '{}'.format(self._year.text())),
                                ('Comment', '{}'.format(self._comment.text()))])

        return data
