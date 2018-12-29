from pathlib import Path

from PySide2.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout, \
    QDesktopWidget, QPushButton, QListWidget, QAbstractItemView, QMessageBox
from tools.text2dict import createGameData


class ImportWindow(QDialog):
    def __init__(self):
        super(ImportWindow, self).__init__()

        self.gamesdata = []

        self.platformListPath = Path("data/vgdb/")
        self.platformList = []
        for file in self.platformListPath.iterdir():
            self.platformList.append(file.stem)

        self.setContentsMargins(5, 5, 5, 5)

        self.lblSelect = QLabel("Select platforms to import from:")

        self.consoleList = QListWidget()
        self.consoleList.addItems(sorted(self.platformList))
        self.consoleList.setSelectionMode(QAbstractItemView.MultiSelection)

        self.btnCancel = QPushButton("Cancel")
        self.btnCancel.clicked.connect(self.close)
        self.btnOK = QPushButton("OK")
        self.btnOK.clicked.connect(self._doImport)

        self.hboxOKCancel = QHBoxLayout()
        self.hboxOKCancel.addStretch(5)
        self.hboxOKCancel.addWidget(self.btnOK, 0)
        self.hboxOKCancel.addWidget(self.btnCancel, 1)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.lblSelect, 0)
        self.vbox.addWidget(self.consoleList, 1)
        self.vbox.addLayout(self.hboxOKCancel, 2)

        self.setLayout(self.vbox)
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
        platforms = [x.text() for x in self.consoleList.selectedItems()]
        proceed = QMessageBox.Ok

        if len(platforms) > 1:
            proceed = QMessageBox.warning(self, "Import warning",
                                                "Importing multiple platforms can take a long time.\n"
                                                "Are you sure you want to proceed?",
                                                QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Cancel)

        if proceed == QMessageBox.Ok:
            newData = []
            for file in self.platformListPath.iterdir():
                if file.stem in platforms:
                    newData.append(createGameData(file))
            for lst in newData:
                for game in lst:
                    self.gamesdata.append(game)
            self.accept()

    def returnData(self):
        return self.gamesdata
