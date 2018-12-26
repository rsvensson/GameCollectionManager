#!/usr/bin/env python
from PySide2.QtCore import Qt, Signal, QModelIndex
from PySide2.QtGui import QFont, QColor
from PySide2.QtSql import QSqlTableModel, QSqlQuery


class TableModel(QSqlTableModel):
    """
    Subclassing QSqlTableModel to be able to customize data in our cells
    http://www.wouterspekkink.org/software/q-sopra/technical/c++/qt/2018/01/19/qsltablemodels-booleans-and-check-boxes.html
    """

    fetched = Signal()

    def __init__(self, *args, **kwargs):
        QSqlTableModel.__init__(self, *args, **kwargs)

    def fetchMore(self, parent=QModelIndex()):
        # So we can detect when more items has been fetched and resize rows. Not working yet.
        self.fetched.emit()
        return super().fetchMore(parent)

    def flags(self, index):
        result = QSqlTableModel.flags(self, index)
        if self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory",
                                                              "Box", "Manual"):
            result |= Qt.ItemIsUserCheckable
        return result

    def data(self, index, role=Qt.DisplayRole):
        """
        TODO: Figure out why bindValue isn't working but format is
        """
        # Handle setting our checkboxes
        if self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory",
                                                              "Box", "Manual"):
            if role == Qt.CheckStateRole:
                query = QSqlQuery()
                table = self.tableName()
                itemID = index.row()
                item = self.headerData(index.column(), Qt.Horizontal)
                query.prepare("SELECT {} FROM {} WHERE ID={}".format(item, table, itemID))
                query.bindValue(":item", item)
                query.bindValue(":itemID", itemID)
                query.exec_()
                query.first()
                result = query.value(0)

                if result == "Yes":
                    return Qt.Checked
                elif result == "No":
                    return Qt.Unchecked
            else:
                return QSqlTableModel.data(self, index, role)
        # Bold fonts
        elif role == Qt.FontRole and self.headerData(index.column(), Qt.Horizontal) in ("Region",
                                                                                        "Country"):
            font = QFont()
            font.setBold(True)
            return font
        # Set foreground color
        elif role == Qt.ForegroundRole and self.headerData(index.column(), Qt.Horizontal) == "Region":
            if index.data() in ("PAL", "Europe"):
                return QColor(255, 255, 0)
            elif index.data() in ("NTSC (JP)", "Japan"):
                return QColor(255, 0, 0)
            elif index.data() in ("NTSC (NA)", "North America"):
                return QColor(0, 0, 255)
        # Set text alignment
        elif role == Qt.TextAlignmentRole \
                and self.headerData(index.column(), Qt.Horizontal) in ("Region", "Country"):
            return Qt.AlignCenter
        # Display the cell data in tooltip
        elif role == Qt.ToolTipRole:
            return QSqlTableModel.data(self, index, Qt.DisplayRole)

        return QSqlTableModel.data(self, index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory",
                                                              "Box", "Manual"):
            if role == Qt.CheckStateRole:
                if value == Qt.Checked:
                    query = QSqlQuery()
                    table = self.tableName()
                    itemID = index.row()
                    item = self.headerData(index.column(), Qt.Horizontal)
                    query.prepare("UPDATE {} SET {}='Yes' WHERE ID={}".format(table, item, itemID))
                    #query.bindValue(":itemID", itemID)
                    #query.bindValue(":item", item)
                    query.exec_()
                    del query
                    return True
                elif value == Qt.Unchecked:
                    query = QSqlQuery()
                    table = self.tableName()
                    itemID = index.row()
                    item = self.headerData(index.column(), Qt.Horizontal)
                    query.prepare("UPDATE {} SET {}='No' WHERE ID={}".format(table, item, itemID))
                    #query.bindValue(":id", id)
                    #query.bindValue(":item", item)
                    query.exec_()
                    del query
                    return True
        return QSqlTableModel.setData(self, index, value, role)
