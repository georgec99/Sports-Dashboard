from db.dbConnection import getConnection
from datetime import date


def createTbl():
    conn = getConnection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS standings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_date TEXT NOT NULL,
            competition_code TEXT NOT NULL,
            position INTEGER,
            team_name TEXT,
            team_short_name TEXT,
            played INTEGER,
            won INTEGER,
            drawn INTEGER,
            lost INTEGER,
            goals_for INTEGER,
            goals_against INTEGER,
            goal_difference INTEGER,
            points INTEGER
        )
    """)

    conn.commit()
    conn.close()
    print("Standings Tables Created")


def saveStandings(competition_code, standings_data):
    conn = getConnection()
    cur = conn.cursor()

    tdyDate = str(date.today())
    for team in standings_data
        cur.execute("INSERT INTO standings (competition_code, snapshot_date") VALUES (,)
