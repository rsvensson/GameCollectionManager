#!/usr/bin/env python
from PySide2.QtCore import Qt
from matplotlib import use
use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import arange
from PySide2.QtWidgets import QWidget, QLabel, QGridLayout, QSizePolicy, QScrollArea, QHBoxLayout, QVBoxLayout


class MplCanvas(FigureCanvas):
    """Shell class for setting up matplotlib"""

    def __init__(self, data, ylabel, parent=None, width=5, height=4, dpi=100):
        self._fig = Figure(figsize=(width, height), dpi=dpi)
        self._ax = self._fig.subplots()
        self._ylabel = ylabel
        self._xlabel = "Platforms"

        self._data = data

        self.computeInitialFigure()

        super(MplCanvas, self).__init__(self._fig)
        self.setParent(parent)

        super().setMinimumSize(self.size())
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

    def _setupBars(self, ax, bars, index, platforms):
        """Settings for bar graphs. Sets up labels, ticks,
           and puts the bar values as text on top of the bars."""
        ax.set_xlabel(self._xlabel)
        ax.set_ylabel(self._ylabel)
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

        self._tables = tables

        self._hbox = QHBoxLayout()
        self._hbox.setAlignment(Qt.AlignLeft)
        self._vboxPlots = QVBoxLayout()
        self._vboxLabels = QVBoxLayout()
        self._vboxLabels.setAlignment(Qt.AlignTop)
        self.scroll = QScrollArea()
        self.scroll.setLayout(self._vboxPlots)
        self._hbox.addLayout(self._vboxLabels)
        self._hbox.addWidget(self.scroll)
        self.widget = QWidget()
        self.widget.setLayout(self._hbox)

        self._lblTables = []  # List of table types (games, consoles, accessories)
        self._platforms = []  # List of platforms from all tables

        # Data for how many items each platform has, for matplotlib
        self._gamesData = {}
        self._consoleData = {}
        self._accessoryData = {}

        self._totalItems = 0

        self._extractData()

        self._lblTotal = QLabel()
        self._lblTotal.setText("Total items in collection: {}".format(self._totalItems))

        self._gd = CollectionDataCanvas(self.layout, self._gamesData, "Games")
        self._cd = CollectionDataCanvas(self.layout, self._consoleData, "Consoles")
        self._ad = CollectionDataCanvas(self.layout, self._accessoryData, "Accessories")

        self._gd.mpl_connect("scroll_event", self._scrolling)
        self._cd.mpl_connect("scroll_event", self._scrolling)
        self._ad.mpl_connect("scroll_event", self._scrolling)

        self._vboxPlots.addWidget(self._gd)
        self._vboxPlots.addWidget(self._cd)
        self._vboxPlots.addWidget(self._ad)
        for label in self._lblTables:
            self._vboxLabels.addWidget(label)
        self._vboxLabels.addWidget(self._lblTotal)

    def _extractData(self):
        tempPlatforms = set()
        for table in self._tables:
            tempPlatforms |= table.platforms()

        for i, table in enumerate(self._tables):
            self._lblTables.append(QLabel())
            self._lblTables[i].setText("Number of {}: {}".format(table.model.tableName(),
                                                                 table.ownedCount()))

        # Counts how many items each platform has and puts it into a dictionary
        self._platforms = sorted(tempPlatforms, key=str.lower)
        for platform in self._platforms:
            self._gamesData[platform] = 0
            self._consoleData[platform] = 0
            self._accessoryData[platform] = 0
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

    def _scrolling(self, event):
        val = self.scroll.verticalScrollBar().value()
        if event.button == "down":
            self.scroll.verticalScrollBar().setValue(val+100)
        else:
            self.scroll.verticalScrollBar().setValue(val-100)
