#!/usr/bin/env python
from PySide2.QtCore import Qt
from PySide2.QtSql import QSqlTableModel, QSqlQuery


class TableModel(QSqlTableModel):
    """
    Subclassing QSqlTableModel to be able to have checkboxes in our cells
    http://www.wouterspekkink.org/software/q-sopra/technical/c++/qt/2018/01/19/qsltablemodels-booleans-and-check-boxes.html
    """
    def __init__(self, *args, **kwargs):
        QSqlTableModel.__init__(self, *args, **kwargs)

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
        if self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory",
                                                              "Box", "Manual"):
            #if role == Qt.CheckStateRole and (self.flags(index) & Qt.ItemIsUserCheckable != Qt.NoItemFlags):
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
        elif role == Qt.ToolTipRole:
            return QSqlTableModel.data(self, index, Qt.DisplayRole)

        return QSqlTableModel.data(self, index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory",
                                                              "Box", "Manual"):
            #if role == Qt.CheckStateRole and (self.flags(index) & Qt.ItemIsUserCheckable != Qt.NoItemFlags):
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
