from pathlib import Path

from PySide2.QtWidgets import QDialog, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout, QDesktopWidget,\
    QPushButton

from tools.text2csv import createCSV


class ImportWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.platformListPaths = Path("data/vgdb/*.txt")
        self.platformList = dict()

        self.setContentsMargins(5, 5, 5, 5)
        self.lblAll = QLabel("All")
        self.all = QCheckBox()
        self.all.setObjectName("All")

        self.btnCancel = QPushButton("Cancel")
        self.btnOK = QPushButton("OK")
        self.btnOK.clicked.connect(self.doImport)

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

    def doImport(self):
        print("Not implemented yet")
