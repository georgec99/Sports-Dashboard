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

    for team in standings_data:

        tblValues=(
            tdyDate,
            competition_code,
            team["position"],
            team["team"]["name"],
            team["team"]["shortName"],
            team["playedGames"],
            team["won"],
            team["draw"],
            team["lost"],
            team["goalsFor"],
            team["goalsAgainst"],
            team["goalDifference"],
            team["points"]
            )
        placeholders = ", ".join(["?"] * len(tblValues))
           
        cur.execute(f"""
        INSERT INTO standings (
            snapshot_date,
            competition_code,
            position,
            team_name,
            team_short_name,
            played,
            won,
            drawn,
            lost,
            goals_for,
            goals_against,
            goal_difference,
            points
        ) VALUES ({placeholders})
        """,tblValues)

    conn.commit()
    conn.close()

    print(f"Saved {len(standings_data)} teams to standings.")

def getLatestStandings(competition_code):
    conn = getConnection()
    cur = conn.cursor()

    cur.execute(("""
        SELECT * FROM standings
        WHERE competition_code = ?
        AND snapshot_date = (SELECT MAX(snapshot_date) FROM standings
                            WHERE competition_code = ?)
        ORDER BY position
                """),(competition_code, competition_code))
    
    rows = cur.fetchall()
    conn.close()
    return rows
    


        