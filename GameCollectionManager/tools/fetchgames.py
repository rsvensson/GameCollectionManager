#!/usr/bin/env python

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen


class TableParser:
    def parse_url(self, url):
        response = requests.get(url)
        soup = bs(response.text, "html.parser")
        return [(table["id"], self.parse_html_table(table))
                for table in soup.find_all("table")]

    def parse_html_table(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []

        for row in table.find_all("tr"):
            td_tags = row.find_all("td")
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    n_columns = len(td_tags)

            th_tags = row.find_all("th")
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

            if len(column_names) > 0 and len(column_names) != n_columns:
                raise Exception("Column titles do not match the number of columns")

            columns = column_names if len(column_names) > 0 else range(0, n_columns)
            df = pd.DataFrame(columns=columns,
                              index=range(n_rows))
            row_marker = 0
            for row in table.find_all("tr"):
                column_marker = 0
                columns = row.find_all("td")
                for column in columns:
                    df.iat[row_marker, column_marker] = column.get_text()
                    column_marker += 1
                if len(columns) > 0:
                    row_marker += 1

            for col in df:
                try:
                    df[col] = df[col].astype(float)
                except ValueError:
                    pass

            return df


# url = "file:///home/synt4x/Code/Projects/GameCollectionManager/" +\
#    "GameCollectionManager/data/html/PS1US.html"
url = "https://web.archive.org/web/20150408124919/http://www.sonyindex.com/Pages/PSone_US_Name.htm"

# table = html.find_all("table")[2]
tp = TableParser()
table = tp.parse_url(url)
table.head()


gamelist = []
