# Imports
import json
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

from balldontlie import BalldontlieAPI

from nba_api.stats.endpoints import playercareerstats, leaguestandings, leaguedashteamstats
from nba_api.stats.static import teams, players
from nba_api.stats.library.parameters import SeasonAll


def main():
    # Calling all functions here
    scrape_get_all_teams()
    scrape_get_all_players_of_all_time()
    scrape_single_player_by_id()
    scrape_player_info_by_full_name()
    scrape_ACTIVE_PLAYERS()
    scrape_team_ratings()


"""
Title: Github NBA API webscrape
"""

"""
1. Getting all teams and offloading them into a csv file
    "nba_teams.csv"
"""
def scrape_get_all_teams():
    
    # getting all teams
    nba_teams = teams.get_teams()

    df = pd.DataFrame(nba_teams)
    df.to_csv('uncleaned_csv/nba_teams.csv')
    df
    
    
    

"""
2. Getting all players of all time
    "all_players.csv"
"""
def scrape_get_all_players_of_all_time():
    all_players = players.get_players()

    df = pd.DataFrame(all_players)
    df.to_csv("uncleaned_csv/all_players.csv")
    df



"""
3. Getting a single player by their id and offloading to a csv file
    "Nikola_Jokic_Info.csv"
"""
def scrape_single_player_by_id():
    career = playercareerstats.PlayerCareerStats(player_id='203999')

    info = career.get_data_frames()[0]
    df = pd.DataFrame(info)
    df.to_csv("uncleaned_csv/Nikola_Jokic_Info.csv")
    df




"""
4. Getting a player's info by their full name to see if the player is active
    "AlexAbrines.csv"
"""
def scrape_player_info_by_full_name():
    # var to get player's info and to see if the player is active
    name = "Alex Abrines"


    # finding playyer by their full name
    player = players.find_players_by_full_name(name)

    df = pd.DataFrame(player)


    # removing whitespaces from player name to be used as a file name (e.g AlexAbrines.csv)
    csv_name = name.replace(" ", "")

    df.to_csv(f"uncleaned_csv/{csv_name}.csv")
    df




"""
Title: Ball don't lie API webscraping
"""


"""
5. Getting all ACTIVE players and offloading to a csv file
    "ACTIVE_PLAYERS.csv"
"""
def scrape_ACTIVE_PLAYERS():

    import requests
    # from google.colab import userdata

    load_dotenv()
    API_KEY = os.getenv('nba_api_key')

    # All 30 NBA teams
    team_ids = list(range(1, 31))

    # Build team_id params
    team_params = "&".join([f"team_ids[]={t}" for t in team_ids])

    url = f"https://api.balldontlie.io/nba/v1/players?{team_params}&per_page=100"

    headers = {
        "Authorization": API_KEY
    }

    # making a request to the api, and then getting a response
    response = requests.get(url, headers=headers)
    data = response.json()

    df = pd.json_normalize(data["data"])

    # offloading to csv file
    df.to_csv("uncleaned_csv/ACTIVE_PLAYERS.csv", index=False)

    print("Active players scraped:", len(df))
    

"""
6. Getting team ratings (Wins, Losses, Defensive Ratings)
    "league_standings.csv"
    "advanced_team_stats.csv"
"""
def scrape_team_ratings():
    # Get current league standings (Wins, Losses)
    standings = leaguestandings.LeagueStandings()
    df_standings = standings.get_data_frames()[0]
    df_standings.to_csv("uncleaned_csv/league_standings.csv")

    # Get advanced team stats (Defensive Rating, Offensive Rating, etc.)
    # measure_type_detailed_defense='Advanced' gets you DEF_RATING
    advanced_stats = leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced')
    df_advanced = advanced_stats.get_data_frames()[0]
    df_advanced.to_csv("uncleaned_csv/advanced_team_stats.csv")

    print("Active players scraped:", len(df_advanced))
    
    



main()