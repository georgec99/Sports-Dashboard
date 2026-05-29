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
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER UNIQUE,
            competition_code TEXT NOT NULL,
            matchday INTEGER,
            match_date TEXT,
            status TEXT,
            home_team TEXT,
            away_team TEXT,
            home_score INTEGER,
            away_score INTEGER,
            winner TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Matches Tables Created")


def savematches(competition_code, matches_data):
    conn = getConnection()
    cur = conn.cursor() 

    for match in matches_data:

        tblValues=(
            get_helper(match,"id", default =0),
            competition_code,
            get_helper(match,"matchday", default =0),
            get_helper(match,"utcDate", default =None), 
            get_helper(match,"status", default=None), 
            get_helper(match,"homeTeam","shortName"), 
            get_helper(match,"awayTeam","shortName"), 
            get_helper(match,"score","fullTime","home"),
            get_helper(match,"score","fullTime","away"),
            get_helper(match,"score","winner", default=None)
        )
        placeholders = ", ".join(["?"] * len(tblValues))
           
        cur.execute(f"""
        INSERT INTO matches (
            match_id,
            competition_code,
            matchday,
            match_date,
            status,
            home_team,
            away_team,
            home_score,
            away_score,
            winner 
        ) VALUES ({placeholders})
        ON CONFLICT(match_id) DO UPDATE SET
            status = excluded.status,
            home_score = excluded.home_score,
            away_score = excluded.away_score,
            winner = excluded.winner
        """,tblValues)

    conn.commit()
    conn.close()

    print(f"Saved {len(matches_data)} teams to matches.")

def getLatestMatches(competition_code):
    conn = getConnection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM matches
        WHERE competition_code = ?
        ORDER BY matchday ASC, match_date ASC
        """,(competition_code,))
    
    rows = cur.fetchall()
    conn.close()
    return rows
