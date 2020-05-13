import csv
from collections import OrderedDict
from PySide2.QtSql import QSqlDatabase


def sql2csv(db: QSqlDatabase, tables: list, filetype: str):
    rows = []

    if not db.isOpen():
        try:
            db.open()
        except Exception as e:
            print(str(e))

    for table in tables:
        query = db.exec_(f"SELECT * FROM {table} ORDER BY Platform ASC, Name ASC")
        while query.next():
            if table == "games":
                rows.append(OrderedDict([("Platform", query.value(1)),
                                         ("Name", query.value(2)),
                                         ("Region", query.value(3)),
                                         ("Code", query.value(4)),
                                         ("Game", query.value(5)),
                                         ("Box", query.value(6)),
                                         ("Manual", query.value(7)),
                                         ("Year", query.value(8)),
                                         ("Comment", query.value(9))]))
            elif table == "consoles":
                rows.append(OrderedDict([("Platform", query.value(1)),
                                         ("Name", query.value(2)),
                                         ("Region", query.value(3)),
                                         ("Country", query.value(4)),
                                         ("Serial number", query.value(5)),
                                         ("Console", query.value(6)),
                                         ("Box", query.value(7)),
                                         ("Manual", query.value(8)),
                                         ("Year", query.value(9)),
                                         ("Comment", query.value(10))]))
            elif table == "accessories":
                rows.append(OrderedDict([("Platform", query.value(1)),
                                         ("Name", query.value(2)),
                                         ("Region", query.value(3)),
                                         ("Country", query.value(4)),
                                         ("Accessory", query.value(5)),
                                         ("Box", query.value(6)),
                                         ("Manual", query.value(7)),
                                         ("Year", query.value(8)),
                                         ("Comment", query.value(9))]))

        with open("{}.{}".format(table, filetype), 'w', encoding='utf8') as f:
            writer = csv.DictWriter(f,
                                    dialect="excel-tab" if filetype == "tsv" else "excel",
                                    fieldnames=list(rows[0].keys()))
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        rows.clear()

