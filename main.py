import requests as r
from tabulate import tabulate as tbl
from dotenv import load_dotenv
import os
import db.standings_tbl as standingsTbl
import db.scorers_tbl as scorersTbl
import db.matches_tbl as matchesTbl


load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_API_URL = "https://api.football-data.org/v4"
headers = {"X-Auth-Token": API_KEY}

def fetchCompID(compCode):
    response = r.get(
        f"{BASE_API_URL}/competitions", headers=headers
        )
    rspComp = response.json()["competitions"]
    for comptetiton in rspComp:
        if comptetiton["code"] == compCode:
            return comptetiton["id"]
    return None

def fetchData(compCode):
    compId = fetchCompID(compCode)

    standings = (r.get(
        f"{BASE_API_URL}/competitions/{compId}/standings", headers=headers
        )
    ).json()

    scorers = (r.get(
        f"{BASE_API_URL}/competitions/{compId}/scorers", headers=headers
        )
    ).json()

    matches = (r.get(
        f"{BASE_API_URL}/competitions/{compId}/matches", headers=headers
        )
    ).json()

    return {
        "standings": standings["standings"][0]["table"],
        "scorers" : scorers["scorers"],
        "matches" : matches["matches"]
    }

def main():

    data = fetchData("PL")

    standingsData = data["standings"]
    scorersData = data["scorers"]
    matchesData = data["matches"]


    rows = []
    for team in standingsData:
        rows.append([
            team["position"],
            team["team"]["shortName"],
            team["playedGames"],
            team["won"],
            team["draw"],
            team["lost"],
            team["goalsFor"],
            team["goalsAgainst"],
            team["goalDifference"],
            team["points"]
        ])

    tabHeaders = ["","Team","P","W","D","L","GF","GA","GD", "Pts"]

    finalTbl = tbl(rows, headers=tabHeaders, tablefmt="rounded_outline" )
    
    standingsTbl.createTbl()
    standingsTbl.saveStandings("PL",standingsData)
    rowsFromDB = standingsTbl.getLatestStandings("PL")
    print(f"Rows saved to database: {len(rowsFromDB)}")

    scorersTbl.createTbl()
    scorersTbl.saveScorers("PL", scorersData)

    matchesTbl.createTbl()
    matchesTbl.savematches("PL", matchesData)

    return finalTbl

print(main())

