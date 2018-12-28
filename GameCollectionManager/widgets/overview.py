#!/usr/bin/env python

from matplotlib import use
use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import arange
from PySide2.QtWidgets import QWidget, QLabel, QGridLayout, QSizePolicy, QScrollArea


class MplCanvas(FigureCanvas):
    """Shell class for setting up matplotlib"""

    def __init__(self, data, ylabel, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.subplots()
        self.ylabel = ylabel
        self.xlabel = "Platforms"

        self.data = data

        self.computeInitialFigure()

        super(MplCanvas, self).__init__(self.fig)
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
        platforms = self.data.keys()
        index = arange(len(platforms))
        for platform in platforms:
            values.append(self.data[platform])

        bars = self.ax.bar(index, values, color="thistle")
        self.setupBars(self.ax, bars, index, platforms)

    def setupBars(self, ax, bars, index, platforms):
        """Settings for bar graphs. Sets up labels, ticks,
           and puts the bar values as text on top of the bars."""
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_xticks(index)
        ax.set_xticklabels(platforms)
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)

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

        self.tables = tables

        self.layout = QWidget()
        self.grid = QGridLayout()
        self.layout.setLayout(self.grid)
        #self.scroll = QScrollArea()
        #self.scroll.setWidget(self.layout)

        self.lblTables = []  # List of table types (games, consoles, accessories)
        self.platforms = []  # List of platforms from all tables

        # Data for how many items each platform has, for matplotlib
        self.gamesData = {}
        self.consoleData = {}
        self.accessoryData = {}

        self.totalItems = 0

        self._extractData()

        self.lblTotal = QLabel()
        self.lblTotal.setText("Total items in collection: {}".format(self.totalItems))

        self.gd = CollectionDataCanvas(self.layout, self.gamesData, "Games")
        self.cd = CollectionDataCanvas(self.layout, self.consoleData, "Consoles")
        self.ad = CollectionDataCanvas(self.layout, self.accessoryData, "Accessories")
        #cd = CollectionDataCanvas(self.layout, width=5, height=4, dpi=100)

        self.grid.addWidget(self.gd, 0, 1)
        for i, label in enumerate(self.lblTables):
            self.grid.addWidget(label, i+1, 0)
        self.grid.addWidget(self.lblTotal, 4, 0)

    def _extractData(self):
        tempPlatforms = set()
        for table in self.tables:
            tempPlatforms |= table.platforms()

        for i, table in enumerate(self.tables):
            self.lblTables.append(QLabel())
            self.lblTables[i].setText("Number of {}: {}".format(table.model.tableName(),
                                                                table.ownedCount()))

        # Counts how many items each platform has and puts it into a dictionary
        self.platforms = sorted(tempPlatforms, key=str.lower)
        for platform in self.platforms:
            self.gamesData[platform] = 0
            self.consoleData[platform] = 0
            self.accessoryData[platform] = 0
        for table in self.tables:
            for platform in self.platforms:
                if table.model.tableName() == "games":
                    self.gamesData[platform] = table.itemsInPlatform(platform)
                elif table.model.tableName() == "consoles":
                    self.consoleData[platform] = table.itemsInPlatform(platform)
                elif table.model.tableName() == "accessories":
                    self.accessoryData[platform] = table.itemsInPlatform(platform)

        for table in self.tables:
            self.totalItems += table.ownedCount()