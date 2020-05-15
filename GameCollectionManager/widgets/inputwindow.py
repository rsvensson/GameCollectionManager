import re
from collections.__init__ import OrderedDict

from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import QDialog, QLabel, QComboBox, QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, \
    QInputDialog, QDesktopWidget, QMessageBox
from utilities.fetchinfo import getMobyInfo


class InputWindow(QDialog):
    """Window where user can enter new data into a table.
       It returns the data formatted into an OrderedDict.
       platforms: the platforms from the currently loaded
                  collection."""

    def __init__(self, parent=None):
        super(InputWindow, self).__init__(parent=parent)

        self.setContentsMargins(5, 5, 5, 5)

        self._platforms = ['1292 Advanced Programmable Video System',
                           '3DO',
                           'APF MP1000/Imagination Machine',
                           'Acorn 32-bit',
                           'Adventure Vision',
                           'Alice 32/90',
                           'Altair 680',
                           'Altair 8800',
                           'Amazon Alexa',
                           'Amiga',
                           'Amiga CD32',
                           'Amstrad CPC',
                           'Amstrad PCW',
                           'Android',
                           'Apple I',
                           'Apple II',
                           'Apple IIgs',
                           'Arcade',
                           'Arcadia 2001',
                           'Arduboy',
                           'Astral 2000',
                           'Atari 2600',
                           'Atari 5200',
                           'Atari 7800',
                           'Atari 8-bit',
                           'Atari ST',
                           'Atom',
                           'BBC Micro',
                           'BREW',
                           'Bally Astrocade',
                           'BeOS',
                           'BlackBerry',
                           'Blu-ray Disc Player',
                           'Browser',
                           'Bubble',
                           'CD-i',
                           'CDTV',
                           'CP/M',
                           'Camputers Lynx',
                           'Casio Loopy',
                           'Casio PV-1000',
                           'Channel F',
                           'ClickStart',
                           'Coleco Adam',
                           'ColecoVision',
                           'Colour Genie',
                           'Commodore 128',
                           'Commodore 16, Plus/4',
                           'Commodore 64',
                           'Commodore PET/CBM',
                           'Compal 80',
                           'Compucolor I',
                           'Compucolor II',
                           'Compucorp Programmable Calculator',
                           'CreatiVision',
                           'DOS',
                           'DVD Player',
                           'Dedicated console',
                           'Dedicated handheld',
                           'Didj',
                           'DoJa',
                           'Dragon 32/64',
                           'Dreamcast',
                           'ECD Micromind',
                           'Electron',
                           'Enterprise',
                           'Epoch Cassette Vision',
                           'Epoch Game Pocket Computer',
                           'Epoch Super Cassette Vision',
                           'ExEn',
                           'Exelvision',
                           'Exidy Sorcerer',
                           'FM Towns',
                           'FM-7',
                           'FRED/COSMAC',
                           'Fire OS',
                           'Freebox',
                           'GIMINI',
                           'GNEX',
                           'GP2X',
                           'GP2X Wiz',
                           'GP32',
                           'GVM',
                           'Galaksija',
                           'Game Boy',
                           'Game Boy Advance',
                           'Game Boy Color',
                           'Game Gear',
                           'Game Wave',
                           'Game.Com',
                           'GameCube',
                           'GameStick',
                           'Genesis',
                           'Gizmondo',
                           'Glulx',
                           'HD DVD Player',
                           'HP 9800',
                           'HP Programmable Calculator',
                           'Heath/Zenith H8/H89',
                           'Heathkit H11',
                           'Hitachi S1',
                           'Hugo',
                           'HyperScan',
                           'IBM 5100',
                           'Ideal-Computer',
                           'Intel 8008',
                           'Intel 8080',
                           'Intellivision',
                           'Interton Video 2000',
                           'J2ME',
                           'Jaguar',
                           'Jolt',
                           'Jupiter Ace',
                           'KIM-1',
                           'Kindle Classic',
                           'Laser 200',
                           'LaserActive',
                           'LeapFrog Explorer',
                           'LeapTV',
                           'Leapster',
                           'Linux',
                           'Lynx',
                           'MOS Technology 6502',
                           'MRE',
                           'MSX',
                           'Macintosh',
                           'Maemo',
                           'Mainframe',
                           'Mattel Aquarius',
                           'MeeGo',
                           'Memotech MTX',
                           'Microbee',
                           'Microtan 65',
                           'Microvision',
                           'Mophun',
                           'Motorola 6800',
                           'Motorola 68k',
                           'N-Gage',
                           'N-Gage (service)',
                           'NES',
                           'Nascom',
                           'Neo Geo',
                           'Neo Geo CD',
                           'Neo Geo Pocket',
                           'Neo Geo Pocket Color',
                           'Neo Geo X',
                           'New Nintendo 3DS',
                           'NewBrain',
                           'Newton',
                           'Nintendo 3DS',
                           'Nintendo 64',
                           'Nintendo DS',
                           'Nintendo DSi',
                           'Nintendo Switch',
                           'North Star',
                           'Noval 760',
                           'Nuon',
                           'OS/2',
                           'Oculus Go',
                           'Oculus Quest',
                           'Odyssey',
                           'Odyssey 2',
                           'Ohio Scientific',
                           'OnLive',
                           'Orao',
                           'Oric',
                           'Ouya',
                           'PC Booter',
                           'PC-6001',
                           'PC-8000',
                           'PC-88',
                           'PC-98',
                           'PC-FX',
                           'PS Vita',
                           'PSP',
                           'Palm OS',
                           'Philips VG 5000',
                           'Photo CD',
                           'Pippin',
                           'PlayStation',
                           'PlayStation 2',
                           'PlayStation 3',
                           'PlayStation 4',
                           'Playdia',
                           'Pokémon Mini',
                           'Pokitto',
                           'Poly-88',
                           'RCA Studio II',
                           'Roku',
                           'SAM Coupé',
                           'SC/MP',
                           'SD-200/270/290',
                           'SEGA 32X',
                           'SEGA CD',
                           'SEGA Master System',
                           'SEGA Pico',
                           'SEGA Saturn',
                           'SG-1000',
                           'SK-VM',
                           'SMC-777',
                           'SNES',
                           'SRI-500/1000',
                           'SWTPC 6800',
                           'Sharp MZ-80B/2000/2500',
                           'Sharp MZ-80K/700/800/1500',
                           'Sharp X1',
                           'Sharp X68000',
                           'Sharp Zaurus',
                           'Signetics 2650',
                           'Sinclair QL',
                           'Sol-20',
                           'Sord M5',
                           'Spectravideo',
                           'Stadia',
                           "Super A'can",
                           'SuperGrafx',
                           'Supervision',
                           'Symbian',
                           'TADS',
                           'TI Programmable Calculator',
                           'TI-99/4A',
                           'TIM',
                           'TRS-80',
                           'TRS-80 CoCo',
                           'TRS-80 MC-10',
                           'Taito X-55',
                           'Tatung Einstein',
                           'Tektronix 4050',
                           'Tele-Spiel ES-2201',
                           'Telstar Arcade',
                           'Terminal',
                           'Thomson MO',
                           'Thomson TO',
                           'Tiki 100',
                           'Timex Sinclair 2068',
                           'Tizen',
                           'Tomahawk F1',
                           'Tomy Tutor',
                           'TurboGrafx CD',
                           'TurboGrafx-16',
                           'V.Flash',
                           'V.Smile',
                           'VIC-20',
                           'VIS',
                           'Vectrex',
                           'VideoBrain',
                           'Videopac+ G7400',
                           'Virtual Boy',
                           'WIPI',
                           'Wang 2200',
                           'Wii',
                           'Wii U',
                           'Windows',
                           'Windows 3.x',
                           'Windows Apps',
                           'Windows Mobile',
                           'Windows Phone',
                           'WonderSwan',
                           'WonderSwan Color',
                           'XaviXPORT',
                           'Xbox',
                           'Xbox 360',
                           'Xbox One',
                           'Xerox Alto',
                           'Z-machine',
                           'ZX Spectrum',
                           'ZX Spectrum Next',
                           'ZX80',
                           'ZX81',
                           'Zeebo',
                           'Zilog Z80',
                           'Zilog Z8000',
                           'Zodiac',
                           'Zune',
                           'bada',
                           'digiBlast',
                           'iPad',
                           'iPhone',
                           'iPod Classic',
                           'tvOS',
                           'watchOS',
                           'webOS']

        self._dataTypes = ["Game", "Console", "Accessory"]
        self._dataTypeLabel = QLabel("Type\t ")
        self._dataType = QComboBox()
        self._dataType.addItems(self._dataTypes)
        self._dataType.currentIndexChanged.connect(self._changeWidgets)

        self._nameLabel = QLabel("Name\t ")
        self._name = QLineEdit()
        self._name.textChanged.connect(self._changeWidgets)

        self._platformLabel = QLabel("Platform\t ")
        self._platform = QComboBox()
        self._platform.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self._platform.addItems(["", "(New platform)"])
        self._platform.addItems(self._platforms)
        self._platform.currentIndexChanged.connect(self._addPlatform)

        self._autofillButton = QPushButton("Autofill")
        self._autofillButton.clicked.connect(self._autofill)
        self._autofillButton.setEnabled(False)

        self._regionLabel = QLabel("Region\t ")
        self._region = QComboBox()
        self._region.addItems(["NTSC (JP)", "NTSC (NA)", "PAL"])

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

        self._genreLabel = QLabel("Genre\t ")
        self._genre = QLineEdit()

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
        self._hboxGenre = QHBoxLayout()
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
        self._hboxGenre.addWidget(self._genreLabel, 0)
        self._hboxGenre.addWidget(self._genre, 1)
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
        self._hboxBtn.addWidget(self._autofillButton, 0, Qt.AlignLeft)
        self._hboxBtn.addStretch(10)
        self._hboxBtn.addWidget(self._okButton, 1)
        self._hboxBtn.addWidget(self._cnclButton, 2)

        self._vbox.addLayout(self._hboxType, 0)
        self._vbox.addLayout(self._hboxName, 1)
        self._vbox.addLayout(self._hboxPlatform, 2)
        self._vbox.addLayout(self._hboxRegion, 3)
        self._vbox.addLayout(self._hboxCode, 4)
        self._vbox.addLayout(self._hboxCountry, 5)
        self._vbox.addLayout(self._hboxYear, 6)
        self._vbox.addLayout(self._hboxGenre, 7)
        self._vbox.addLayout(self._hboxComment, 8)
        self._vbox.addLayout(self._hboxBoxMan, 9)
        self._vbox.addLayout(self._hboxBtn, 10)

        self.setLayout(self._vbox)

        self.setWindowTitle("Add to collection")
        self.setFixedSize(QSize(500, 280))
        self._center()

    def _addPlatform(self):
        if (self._platform.currentText() not in ("", "(New platform)") and
                self._name.text() != "" and not self._name.text().isspace()):
            self._autofillButton.setEnabled(True)
        else:
            self._autofillButton.setEnabled(False)

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
                        # self._platform.removeItem(self._platform.findText(" "))  # Remove the temp empty item if any
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
            if (self._name.text() != "" and not self._name.text().isspace() and
                    self._platform.currentText() not in ("", "(New platform)")):
                self._autofillButton.setEnabled(True)
            else:
                self._autofillButton.setEnabled(False)
        elif self._dataType.currentIndex() == 1:
            self._codeLabel.setEnabled(True)
            self._code.setEnabled(True)
            self._countryLabel.setEnabled(True)
            self._country.setEnabled(True)
            self._codeLabel.setText("Serial No\t ")
            self._itemLabel.setText("Console")
            self._autofillButton.setEnabled(False)
        elif self._dataType.currentIndex() == 2:
            self._countryLabel.setEnabled(True)
            self._country.setEnabled(True)
            self._codeLabel.setEnabled(False)
            self._code.setEnabled(False)
            self._itemLabel.setText("Accessory")
            self._autofillButton.setEnabled(False)

    def _autofill(self):
        name = self._name.text()
        platform = self._platform.currentText()
        regionDict = {"NTSC (JP)": ("Japan", "Worldwide"),
                      "NTSC (NA)": ("United States", "Canada", "Worldwide"),
                      "PAL": ("United Kingdom", "Ireland", "Germany", "France", "Italy",
                              "Austria", "Belgium", "The Netherlands", "Portugal",
                              "Spain", "Switzerland", "Russia",
                              "Sweden", "Denmark", "Norway", "Finland",
                              "Australia, New Zealand", "Worldwide")}
        region = regionDict[self._region.currentText()]

        if name == "" or platform == "" or name.isspace() or platform.isspace():
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setWindowTitle("Missing data")
            msgBox.setText("<h2>Missing data</h2>")
            msgBox.setInformativeText("Please enter both a name and a platform.")
            msgBox.exec_()
        else:
            info = getMobyInfo(name, platform)
            if info["title"] == "":
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("No info found")
                msgBox.setText("<h2>No info found</h2>")
                msgBox.setInformativeText("Couldn't find any info on that title. Is the spelling and platform correct?")
                msgBox.exec_()
                return

            yearFormat = re.compile(r"\d{4}")
            year = yearFormat.findall(info["release"])
            genre = info["genre"]
            code = ""

            # Try to get product code
            for release, details in zip(info["releases"].keys(), info["releases"].values()):
                correctRelease = False

                if region == "PAL" and "United Kingdom" in release:
                    # TODO: Make the UK release be the default one if we select PAL
                    pass

                for r in release:
                    if r in region or r == region:
                        correctRelease = True
                        break

                if correctRelease:
                    for d in details:
                        if d[0] in ("Company Code", "Nintendo Media PN", "Sony PN"):
                            code = d[1]
                            break
                if code != "":
                    break

            # Try with EAN-13 or UPC-A as a fallback
            if code == "":
                for release, details in zip(info["releases"].keys(), info["releases"].values()):
                    for d in details:
                        if d[0] in ("EAN-13", "UPC-A"):
                            code = d[1]
                            break
                    if code != "":
                        break

            if year == "" and code == "":
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("No info found")
                msgBox.setText("<h2>No info found</h2>")
                msgBox.setInformativeText("Sorry, couldn't find any info about this title.")
                msgBox.exec_()
            else:
                self._year.setText(year[0])
                self._code.setText(code)
                self._genre.setText(genre)

    def returnData(self):
        data = None

        if self._dataType.currentIndex() == 0:
            data = OrderedDict([('Platform', '{}'.format(self._platform.currentText())),
                                ('Name', '{}'.format(self._name.text())),
                                ('Region', '{}'.format(self._region.currentText())),
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
