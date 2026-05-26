import sqlite3 as sql

DB_PATH = "sports-dashboard.db"

def getConnection():
    conn = sql.connect(DB_PATH)
    conn.row_factory = sql.Row  #Access rows by name
    return conn