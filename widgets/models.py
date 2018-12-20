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
        if self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory", "Box", "Manual"):
            return QSqlTableModel.flags(self, index) | Qt.ItemIsUserCheckable
        else:
            return QSqlTableModel.flags(self, index)

    def data(self, index, role=Qt.DisplayRole):
        """
        TODO: Figure out why bindValue isn't working but format is
        """
        if self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory", "Box", "Manual"):
            if role == Qt.CheckStateRole:
                query = QSqlQuery()
                table = self.tableName()
                id = index.row()
                item = self.headerData(index.column(), Qt.Horizontal)
                query.prepare("SELECT {} FROM {} WHERE ID={}".format(item, table, id))
                #query.bindValue(":item", item)
                #query.bindValue(":id", id)
                query.exec_()
                query.first()
                result = query.value(0)

                if result == "Yes":
                    return Qt.Checked
                elif result == "No":
                    return Qt.Unchecked
                else:
                    return ""
            else:
                return ""
        elif role == Qt.ToolTipRole:
            return QSqlTableModel.data(self, index, Qt.DisplayRole)
        else:
            return QSqlTableModel.data(self, index, role)

    def setData(self, index, value, role):
        """
        TODO: Figure out why it doesn't actually change the table data
        """
        if self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory", "Box", "Manual"):
            if role == Qt.CheckStateRole:
                if value == Qt.Checked:
                    query = QSqlQuery()
                    id = index.row()
                    table = self.tableName()
                    item = self.headerData(index.column(), Qt.Horizontal)
                    query.prepare("UPDATE {} SET {}=Yes WHERE ID={}".format(table, item, id))
                    #query.bindValue(":id", id)
                    #query.bindValue(":item", item)
                    query.exec_()
                    del query
                    print("Test")
                    return True
                elif value == Qt.Unchecked:
                    query = QSqlQuery()
                    id = index.row()
                    table = self.tableName()
                    item = self.headerData(index.column(), Qt.Horizontal)
                    query.prepare("UPDATE {} SET {}=No WHERE ID={}".format(table, item, id))
                    #query.bindValue(":id", id)
                    #query.bindValue(":item", item)
                    query.exec_()
                    del query
                    return True
        return QSqlTableModel.setData(self, index, value, role)
