#!/usr/bin/env python
from PySide2.QtCore import Qt
from matplotlib import use
use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import arange
from PySide2.QtWidgets import QWidget, QLabel, QSizePolicy, QScrollArea, QHBoxLayout, QVBoxLayout


class MplCanvas(FigureCanvas):
    """Shell class for setting up matplotlib"""

    def __init__(self, data, ylabel, parent=None, width=10, height=4, dpi=100):
        self._fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self._ax = self._fig.subplots()
        self._ylabel = ylabel
        self._xlabel = "Platforms"

        self._data = data

        self.computeInitialFigure()

        super(MplCanvas, self).__init__(self._fig)
        self.setParent(parent)

        super().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        super().updateGeometry()

    def computeInitialFigure(self):
        pass


class CollectionDataCanvas(MplCanvas):
    """Collection data-specific matplotlib class"""
    def __init__(self, data, ylabel, *args, **kwargs):
        super(CollectionDataCanvas, self).__init__(ylabel, *args, **kwargs)

    def computeInitialFigure(self):

        values = []
        platforms = self._data.keys()
        index = arange(len(platforms))
        for platform in platforms:
            values.append(self._data[platform])

        bars = self._ax.bar(index, values, color="thistle")
        self._setupBars(self._ax, bars, index, platforms)

    def updateFigure(self, data):
        self._ax.cla()

        values = []
        platforms = data.keys()
        index = arange(len(platforms))
        for platform in platforms:
            values.append(data[platform])

        bars = self._ax.bar(index, values, color="thistle")
        self._setupBars(self._ax, bars, index, platforms)
        self.draw()

    def _setupBars(self, ax, bars, index, platforms):
        """Settings for bar graphs. Sets up labels, ticks,
           and puts the bar values as text on top of the bars."""
        ax.set_title(f"{self._ylabel} per platform")
        ax.set_xlabel(self._xlabel)
        ax.set_ylabel(self._ylabel)
        ax.set_xticks(index)
        ax.set_xticklabels(platforms, rotation=45, ha='right')

        max_y_value = 0
        # Since max() doesn't seem to work with PyInstaller!?
        for bar in bars:
            if bar.get_height() > max_y_value:
                max_y_value = bar.get_height()
        distance = max_y_value * 0.05

        for bar in bars:
            text = bar.get_height()
            text_x = bar.get_x() + bar.get_width() / 2
            text_y = bar.get_height() - distance

            ax.text(text_x, text_y, text, ha='center', va='bottom')


class Overview(QWidget):
    """Overview widget for displaying info about the loaded collection
       tables: The Table objects to display.
       hideNotOwned: bool passed in so we can use table search method properly"""

    def __init__(self, tables):
        super(Overview, self).__init__()

        self.widget = QWidget()

        self._tables = tables
        # Data for how many items each platform has, for matplotlib
        self._gamesData = {}
        self._consoleData = {}
        self._accessoryData = {}
        self._totalItems = 0
        self._lblTables = []  # List of table type labels (games, consoles, accessories)
        self._platforms = []  # List of platforms from all tables
        self._extractData()  # Populate variables above with data
        self._lblTotal = QLabel()
        self._lblTotal.setText(f"Total items in collection: {self._totalItems}")

        # Canvas plots
        self._gd = CollectionDataCanvas(self.widget, self._gamesData, "Games")
        self._cd = CollectionDataCanvas(self.widget, self._consoleData, "Consoles")
        self._ad = CollectionDataCanvas(self.widget, self._accessoryData, "Accessories")

        # Layouts
        self._vboxPlots = QVBoxLayout()
        self._vboxLabels = QVBoxLayout()
        self._vboxLabels.setAlignment(Qt.AlignTop)
        self._vboxPlots.addWidget(self._gd)
        self._vboxPlots.addWidget(self._cd)
        self._vboxPlots.addWidget(self._ad)
        for label in self._lblTables:
            self._vboxLabels.addWidget(label)
        self._vboxLabels.addWidget(self._lblTotal)

        self._plotWidget = QWidget()
        self._plotWidget.setLayout(self._vboxPlots)
        self._scroll = QScrollArea()
        self._scroll.setWidget(self._plotWidget)

        self._hbox = QHBoxLayout()
        self._hbox.setAlignment(Qt.AlignLeft)
        self._hbox.addLayout(self._vboxLabels)
        self._hbox.addWidget(self._scroll)

        self.widget.setLayout(self._hbox)

    def _extractData(self):
        tempPlatforms = set()
        for table in self._tables:
            tempPlatforms |= table.platforms()

        for i, table in enumerate(self._tables):
            self._lblTables.append(QLabel())
            self._lblTables[i].setText(f"Number of {table.model.tableName()}: {table.ownedCount()}")

        # Counts how many items each platform has and puts it into a dictionary
        self._platforms = sorted(tempPlatforms, key=str.lower)
        for table in self._tables:
            for platform in self._platforms:
                if table.model.tableName() == "games":
                    self._gamesData[platform] = table.itemsInPlatform(platform)
                elif table.model.tableName() == "consoles":
                    self._consoleData[platform] = table.itemsInPlatform(platform)
                elif table.model.tableName() == "accessories":
                    self._accessoryData[platform] = table.itemsInPlatform(platform)

        for table in self._tables:
            self._totalItems += table.ownedCount()

    def updateData(self, table):
        if table.model.tableName() == "games":
            self._gamesData.clear()
            self._lblTables[0].setText(f"Number of games: {table.ownedCount()}")
            for platform in sorted(table.platforms(), key=str.lower):
                self._gamesData[platform] = table.itemsInPlatform(platform)
            self._gd.updateFigure(self._gamesData)
        elif table.model.tableName() == "consoles":
            self._consoleData.clear()
            self._lblTables[1].setText(f"Number of consoles: {table.ownedCount()}")
            for platform in sorted(table.platforms(), key=str.lower):
                self._consoleData[platform] = table.itemsInPlatform(platform)
            self._cd.updateFigure(self._consoleData)
        elif table.model.tableName() == "accessories":
            self._accessoryData.clear()
            self._lblTables[2].setText(f"Number of accessories: {table.ownedCount()}")
            for platform in sorted(table.platforms(), key=str.lower):
                self._accessoryData[platform] = table.itemsInPlatform(platform)
            self._ad.updateFigure(self._accessoryData)

        self._totalItems = 0
        for tbl in self._tables:
            self._totalItems += tbl.ownedCount()
        self._lblTotal.setText(f"Total items in collection: {self._totalItems}")
