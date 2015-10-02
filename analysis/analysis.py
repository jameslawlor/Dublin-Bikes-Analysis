import pandas as pd
import sqlite3
import os

for db in os.listdir(os.getcwd()):
    if db.endswith(".db"):
        with sqlite3.connect(db) as con:
            df_bikes = pd.read_sql_query("SELECT * FROM bikes", con)
            df_weather = pd.read_sql_query("SELECT * FROM weather", con)

print df_weather["Weather"]
