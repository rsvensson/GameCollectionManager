from pathlib import Path

from PySide2.QtWidgets import QDialog, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout,\
    QDesktopWidget, QPushButton
from tools.text2dict import createGameData


class ImportWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.gamesdata = []

        self.platformListPath = Path("data/vgdb/")
        self.platformList = dict()

        self.setContentsMargins(5, 5, 5, 5)
        self.lblAll = QLabel("All")
        self.all = QCheckBox()
        self.all.setObjectName("All")

        self.btnCancel = QPushButton("Cancel")
        self.btnCancel.clicked.connect(self.close)
        self.btnOK = QPushButton("OK")
        self.btnOK.clicked.connect(self._doImport)
        self.btnOK.clicked.connect(self.accept)

        self.hboxAll = QHBoxLayout()
        self.hboxAll.addWidget(self.lblAll, 0)
        self.hboxAll.addWidget(self.all, 1)
        self.hboxOKCancel = QHBoxLayout()
        self.hboxOKCancel.addStretch(5)
        self.hboxOKCancel.addWidget(self.btnCancel, 0)
        self.hboxOKCancel.addWidget(self.btnOK, 1)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hboxAll, 0)
        self.vbox.addLayout(self.hboxOKCancel, 1)

        self.checkboxList = [self.all]

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
        if self.all.isChecked():
            newData = []
            for file in self.platformListPath.iterdir():
                newData.append(createGameData(file))
            for lst in newData:
                for game in lst:
                    self.gamesdata.append(game)

    def returnData(self):
        return self.gamesdata
