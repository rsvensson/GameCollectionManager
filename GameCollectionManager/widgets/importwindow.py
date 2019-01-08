from pathlib import Path

from PySide2.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout, \
    QDesktopWidget, QPushButton, QListWidget, QAbstractItemView, QMessageBox
from tools.text2dict import createGameData


class ImportWindow(QDialog):
    def __init__(self):
        super(ImportWindow, self).__init__()

        self.setContentsMargins(5, 5, 5, 5)

        self._gamesdata = []

        self._platformListPath = Path("data/vgdb/")
        self._platformList = []
        for file in self._platformListPath.iterdir():
            self._platformList.append(file.stem)

        self._lblSelect = QLabel("Select platforms to import from:")

        self._consoleList = QListWidget()
        self._consoleList.addItems(sorted(self._platformList))
        self._consoleList.setSelectionMode(QAbstractItemView.MultiSelection)

        self._btnCancel = QPushButton("Cancel")
        self._btnCancel.clicked.connect(self.close)
        self._btnOK = QPushButton("OK")
        self._btnOK.clicked.connect(self._doImport)

        self._hboxOKCancel = QHBoxLayout()
        self._hboxOKCancel.addStretch(5)
        self._hboxOKCancel.addWidget(self._btnOK, 0)
        self._hboxOKCancel.addWidget(self._btnCancel, 1)

        self._vbox = QVBoxLayout()
        self._vbox.addWidget(self._lblSelect, 0)
        self._vbox.addWidget(self._consoleList, 1)
        self._vbox.addLayout(self._hboxOKCancel, 2)

        self.setLayout(self._vbox)
        self.setWindowTitle("Import games")
        self.setFixedSize(500, 280)
        self._center()

    def _center(self):
        """Centers window on screen"""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _doImport(self):
        platforms = [x.text() for x in self._consoleList.selectedItems()]
        proceed = QMessageBox.Ok

        if len(platforms) > 1:
            proceed = QMessageBox.warning(self, "Import warning",
                                                "Importing multiple platforms can take a long time.\n"
                                                "Are you sure you want to proceed?",
                                                QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Cancel)

        if proceed == QMessageBox.Ok:
            newData = []
            for file in self._platformListPath.iterdir():
                if file.stem in platforms:
                    newData.append(createGameData(file))
            for lst in newData:
                for game in lst:
                    self._gamesdata.append(game)
            self.accept()

    def returnData(self):
        return self._gamesdata
