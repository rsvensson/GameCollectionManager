from pathlib import Path

from PySide2.QtWidgets import QDialog, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout


class ImportWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.platformList = Path("data/vgdb/*.txt")

        self.setContentsMargins(5, 5, 5, 5)
        self.lblAll = QLabel("All")
        self.all = QCheckBox()

        self.hboxAll = QHBoxLayout()
        self.hboxAll.addWidget(self.lblAll, 0)
        self.hboxAll.addWidget(self.all, 1)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hboxAll, 0)

