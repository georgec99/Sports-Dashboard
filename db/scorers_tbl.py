from db.dbConnection import getConnection
from datetime import date

#Helper function to handle nested/ null values
def get_helper(obj, *keys, default=0):
    for key in keys:
        if isinstance(obj, dict):
            obj = obj.get(key)
        else:
            return default
    return obj if obj is not None else default

def createTbl():
    conn = getConnection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS scorers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_date TEXT NOT NULL,
            competition_code TEXT NOT NULL,
            player_name TEXT NOT NULL,
            team_name TEXT NOT NULL,
            played_matches INTEGER,
            goals_scored INTEGER,
            assists INTEGER,
            penalties INTEGER,
            UNIQUE(snapshot_date, competition_code, player_name)
        )
    """)

    conn.commit()
    conn.close()
    print("Scorers Table Created")


def saveScorers(competition_code, scorers_data):
    conn = getConnection()
    cur = conn.cursor()

    tdyDate = str(date.today())  

    for scorer in scorers_data:

        tblValues=(
            tdyDate,
            competition_code,
            get_helper(scorer,"player","name", default =None),
            get_helper(scorer,"team","name", default =None),
            get_helper(scorer,"playedMatches"),
            get_helper(scorer,"goals"),
            get_helper(scorer,"assists"),
            get_helper(scorer,"penalties")
        )
        placeholders = ", ".join(["?"] * len(tblValues))
           
        cur.execute(f"""
        INSERT INTO scorers (
            snapshot_date,
            competition_code,
            player_name,
            team_name,
            played_matches,
            goals_scored,
            assists,
            penalties 
        ) VALUES ({placeholders})
        ON CONFLICT (snapshot_date, competition_code, player_name) DO NOTHING
        """,tblValues)

    conn.commit()
    conn.close()

    print(f"Saved {len(scorers_data)} players to scorers.")

def getLatestScorers(competition_code):
    conn = getConnection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM scorers
        WHERE competition_code = ?
        AND snapshot_date = (SELECT MAX(snapshot_date) FROM scorers
                            WHERE competition_code = ?)
        ORDER BY goals_scored DESC
                """,(competition_code, competition_code))
    
    rows = cur.fetchall()
    conn.close()
    return rows
