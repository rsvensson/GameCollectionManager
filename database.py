#/usr/bin/env python

import sqlite3

class Database:
    def __init__(self, file="testdb.db"):
        try:
            self.conn = sqlite3.connect(file)
        except Error as e:
            print(e)
        finally:
            self.conn.close()



db = Database()
