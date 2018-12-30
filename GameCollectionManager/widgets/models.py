#!/usr/bin/env python
from PySide2.QtCore import Qt, Signal, QModelIndex, QSortFilterProxyModel
from PySide2.QtGui import QFont, QColor
from PySide2.QtSql import QSqlTableModel, QSqlQuery


class CheckableSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        QSortFilterProxyModel.__init__(self, parent=parent)

        self.yesNoColumns = []

    def setParameters(self, checkboxCols):
        self.yesNoColumns.clear()

        if len(self.yesNoColumns) > 0:
            for col in checkboxCols:
                self.yesNoColumns.append(col)

    def data(self, index, role=Qt.DisplayRole):
        if index.column() in self.yesNoColumns and (role == Qt.CheckStateRole or role == Qt.DisplayRole):
            if role == Qt.CheckStateRole:
                if index.data(Qt.EditRole) == "Yes":
                    return Qt.Checked
                elif index.data(Qt.EditRole) == "No":
                    return Qt.Unchecked
            elif role == Qt.DisplayRole:
                return QSortFilterProxyModel.data(self, index, role)
        else:
            return QSortFilterProxyModel.data(self, index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if index.column() in self.yesNoColumns and role == Qt.CheckStateRole:
            data = 1 if value == Qt.Checked else 0
            return QSortFilterProxyModel.setData(index, data, Qt.EditRole)
        else:
            return QSortFilterProxyModel.setData(index, value, role)

    def flags(self, index):
        if index.column() in self.yesNoColumns:
            return Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled
        else:
            return QSortFilterProxyModel.flags(index)


class TableModel(QSqlTableModel):
    """
    Subclassing QSqlTableModel to be able to customize data in our cells
    """

    def __init__(self, *args, **kwargs):
        super(TableModel, self).__init__(*args, **kwargs)

    def flags(self, index):
        if self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory",
                                                              "Box", "Manual"):
            #return Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
            return super().flags(index) | Qt.ItemIsUserCheckable
        else:
            return super().flags(index)

    def data(self, index, role=Qt.DisplayRole):
        # Handle setting our checkboxes
        if (role == Qt.CheckStateRole or role == Qt.DisplayRole)\
            and self.headerData(index.column(), Qt.Horizontal) in\
                ("Game", "Console", "Accessory", "Box", "Manual"):

            if role == Qt.CheckStateRole:
                if index.data(Qt.EditRole) == "Yes":
                    return Qt.Checked
                elif index.data(Qt.EditRole) == "No":
                    return Qt.Unchecked
            elif role == Qt.DisplayRole:
                # Display text next to checkboxes
                return super().data(index, role)
                # No text
                # return ""
        # Bold fonts
        elif role == Qt.FontRole and self.headerData(index.column(), Qt.Horizontal) in \
                ("Region", "Country", "Game", "Console", "Accessory", "Box", "Manual"):
            font = QFont()
            font.setBold(True)
            return font
        # Set foreground color
        elif role == Qt.ForegroundRole:
            if self.headerData(index.column(), Qt.Horizontal) == "Region":
                if index.data() in ("PAL", "PAL B", "Europe"):
                    return QColor(255, 255, 0)
                elif index.data() in ("NTSC (JP)", "Japan"):
                    return QColor(255, 0, 0)
                elif index.data() in ("NTSC (NA)", "North America"):
                    return QColor(0, 0, 255)
            elif self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory",
                                                                    "Box", "Manual"):
                if index.data(Qt.EditRole) == "Yes":
                    return QColor(0, 255, 0)
                elif index.data(Qt.EditRole) == "No":
                    return QColor(255, 0, 0)
        # Set text alignment
        elif role == Qt.TextAlignmentRole \
                and self.headerData(index.column(), Qt.Horizontal) in ("Region", "Country"):
            return Qt.AlignCenter
        # Display the cell data in tooltip
        #elif role == Qt.ToolTipRole:
        #    return super().data(index, Qt.DisplayRole)

        return super().data(index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole\
                and self.headerData(index.column(), Qt.Horizontal) in \
                ("Game", "Console", "Accessory", "Box", "Manual"):
            data = "Yes" if value == Qt.Checked else "No"
            return super().setData(index, data, Qt.EditRole)
        else:
            return super().setData(index, value, role)
