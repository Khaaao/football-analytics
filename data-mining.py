from dotenv import load_dotenv
import os
import json
import csv

# Load env params
load_dotenv()

# print(os.getenv("X-RAPIDAPI-KEY"))

current_id_league = ["2", "4"]
old_id_league = ["37", "56", "23", "22"]

# Refactor with Try ?
if not (os.path.isfile('data/football_data.csv')):
    # Create array of league_id of every followed league
    full_retrieve = old_id_league + current_id_league
    # Create csv doc
    with open('data/football_data.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # TODO add league info
        spamwriter.writerow(["league_id", "fixture_id", "round","team_id", "team_name", "player_id", "player_name", "player_position", "player_rating", "player_minutes_played", "player_is_substitute", "shots_total", "shots_on", "goals_total", "goals_conceded", "goal_assists", "passes_total", "passes_key", "passes_accuracy", "tackles_total", "tackles_blocks", "tackles_interceptions", "duels_total", "duels_won", "dribbles_total", "dribbles_attempts", "dribbles_success", "dribbles_past", "fouls_drawn", "fouls_committed", "cards_yellow", "cards_red", "penalty_won", "penalty_commited", "penalty_missed", "penalty_saved", "penalty_success"])
        for league_id in full_retrieve:
            # Mock api call
            with open(f'mock/league.json') as infile:
                league_data = json.load(infile)
                for fixture in league_data["api"]["fixtures"]:
                    # use fixture to call api players/{fixtures_id}
                    # mock api call
                    with open(f'mock/players.json') as infileplayers:
                        players_data = json.load(infileplayers)
                        for player in players_data["api"]["players"]:
                            spamwriter.writerow([league_id, fixture["fixture_id"], fixture["round"] ,player["team_id"], player["team_name"], player["player_id"], player["player_name"], player["position"], player["rating"], player["minutes_played"], player["substitute"], player["shots"]["total"], player["shots"]["on"], player["goals"]["total"],  player["goals"]["conceded"], player["goals"]["assists"], player["passes"]["total"], player["passes"]["key"], player["passes"]["accuracy"], player["tackles"]["total"], player["tackles"]["blocks"], player["tackles"]["interceptions"], player["duels"]["total"], player["duels"]["won"], player["dribbles"]["attempts"], player["dribbles"]["success"], player["dribbles"]["past"], player["fouls"]["drawn"], player["fouls"]["committed"], player["cards"]["yellow"], player["cards"]["red"], player["penalty"]["won"], player["penalty"]["commited"], player["penalty"]["success"], player["penalty"]["missed"], player["penalty"]["saved"]])
                break


else:
    for league in current_id_league:
        print(league)
