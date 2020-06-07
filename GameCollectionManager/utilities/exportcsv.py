import csv

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
                rows.append({"platform":    query.value(1),
                             "name":        query.value(2),
                             "region":      query.value(3),
                             "code":        query.value(4),
                             "game":        query.value(5),
                             "box":         query.value(6),
                             "manual":      query.value(7),
                             "year":        query.value(8),
                             "genre":       query.value(9),
                             "comment":     query.value(10),
                             "publisher":   query.value(11),
                             "developer":   query.value(12),
                             "platforms":   query.value(13)}
                            )
            elif table == "consoles":
                rows.append({"platform":        query.value(1),
                             "name":            query.value(2),
                             "region":          query.value(3),
                             "country":         query.value(4),
                             "serial number":   query.value(5),
                             "console":         query.value(6),
                             "box":             query.value(7),
                             "manual":          query.value(8),
                             "year":            query.value(9),
                             "comment":         query.value(10)}
                            )
            elif table == "accessories":
                rows.append({"platform":    query.value(1),
                             "name":        query.value(2),
                             "region":      query.value(3),
                             "country":     query.value(4),
                             "accessory":   query.value(5),
                             "box":         query.value(6),
                             "manual":      query.value(7),
                             "year":        query.value(8),
                             "comment":     query.value(9)}
                            )

        with open(f"{table}.{filetype}", 'w', encoding='utf8') as f:
            writer = csv.DictWriter(f,
                                    dialect="excel-tab" if filetype == "tsv" else "excel",
                                    fieldnames=list(rows[0].keys()))
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        rows.clear()
