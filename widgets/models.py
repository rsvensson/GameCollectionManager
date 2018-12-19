#!/usr/bin/env python
from PySide2.QtCore import Qt
from PySide2.QtSql import QSqlTableModel, QSqlQuery, QSqlDatabase


class TableModel(QSqlTableModel):
    """
    Subclassing QSqlTableModel to be able to have checkboxes in our cells
    Adapted from https://stackoverflow.com/questions/48193325/checkbox-in-qlistview-using-qsqltablemodel
    with additional info from
    http://www.wouterspekkink.org/software/q-sopra/technical/c++/qt/2018/01/19/qsltablemodels-booleans-and-check-boxes.html
    """
    def __init__(self, *args, **kwargs):
        QSqlTableModel.__init__(self, *args, **kwargs)
        self.checkableData = {}

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
                print(table, id, item)
                query.prepare("SELECT {} FROM {} WHERE ID={}".format(item, table, id))
                #query.bindValue(0, item)
                #query.bindValue(1, id)
                query.exec_()
                query.first()
                result = query.value(0)
                print(result)

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

        #if role == Qt.CheckStateRole and (self.flags(index)&Qt.ItemIsUserCheckable != Qt.NoItemFlags):
        #    if index.row() not in self.checkableData.keys():
        #        # Need to work out logic for checking contents and setting checkbox accordingly
        #        if self.data(index) == "Yes":
        #            print(self.data(index))
        #            self.setData(index, Qt.Checked, Qt.CheckStateRole)
        #        elif self.data(index) == "No":
        #            print(self.data(index))
        #            self.setData(index, Qt.Unchecked, Qt.CheckStateRole)
        #    return self.checkableData[index.row()]
        # else:
        #    return QSqlTableModel.data(self, index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if (self.headerData(index.column(), Qt.Horizontal) in ("Game", "Console", "Accessory", "Box", "Manual")
                and role == Qt.CheckStateRole):
            if value == Qt.Checked:
                query = QSqlQuery()
                id = index.row()
                table = self.tableName()
                item = self.headerData(index.column(), Qt.Horizontal)
                query.prepare("UPDATE '{}' SET :item='Yes' WHERE ID=:id".format(table))
                query.bindValue(":id", id)
                query.bindValue(":item", item)
                query.exec_()
                del query
                return True
            elif value == Qt.Unchecked:
                query = QSqlQuery()
                id = index.row()
                table = self.tableName()
                item = self.headerData(index.column(), Qt.Horizontal)
                query.prepare("UPDATE '{}' SET :item='No' WHERE ID=:id".format(table))
                query.bindValue(":id", id)
                query.bindValue(":item", item)
                query.exec_()
                del query
                return True
        return QSqlTableModel.setData(index, value, role)

    #def setData(self, index, value, role=Qt.EditRole):
    #    if role == Qt.CheckStateRole and (self.flags(index)&Qt.ItemIsUserCheckable != Qt.NoItemFlags):
    #        self.checkableData[index.row()] = value
    #        self.dataChanged.emit(index, index, (role,))
    #        return True
    #    return QSqlTableModel.setData(self, index, value, role)