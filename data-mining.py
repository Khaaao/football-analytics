from dotenv import load_dotenv
import os
import json
import csv
import requests

# Load env params
load_dotenv()

# print(os.getenv("X-RAPIDAPI-KEY"))
# print(os.getenv("THROTTLING"))

THROTTLING = 2
curr_throttling = 0
headers = {'Content-Type': 'application/json', 'x-rapidapi-key': os.getenv("X-RAPIDAPI-KEY")}

########
# TODO DYNAMAC FIXTURE UPLOAD
########

def is_done(league_id):
    pass

if not (os.path.isfile('data/football_data.csv')):
    with open('data/football_data.csv', 'w', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # TODO add league info
        spamwriter.writerow(["league_id", "fixture_id", "round","team_id", "team_name", "player_id", "player_name", "player_position", "player_rating", "player_minutes_played", "player_is_substitute", "shots_total", "shots_on", "goals_total", "goals_conceded", "goal_assists", "passes_total", "passes_key", "passes_accuracy", "tackles_total", "tackles_blocks", "tackles_interceptions", "duels_total", "duels_won", "dribbles_total", "dribbles_attempts", "dribbles_success", "dribbles_past", "fouls_drawn", "fouls_committed", "cards_yellow", "cards_red", "penalty_won", "penalty_commited", "penalty_missed", "penalty_saved", "penalty_success"])
        with open('data/followed_leagues.json') as followed_leagues_json:
            followed_leagues_data = json.load(followed_leagues_json)
            for followed_league in followed_leagues_data:
                if followed_league["is_curent"] == 0:
                    if not (os.path.isfile(f'data/fixtures_{followed_league["league_id"]}.json')):
                        pass
                        # https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{followed_league["league_id"]}
                    else:
                        with open(f'data/fixtures_{followed_league["league_id"]}.json', 'r') as fixtures_json:
                            fixtures_data = json.load(fixtures_json)
                            for num, fixture in enumerate(reversed(fixtures_data["api"]["fixtures"]), start=1):
                                inverse_num = len(fixtures_data["api"]["fixtures"]) - num
                                if not 'is_integrated' in fixture:
                                    if curr_throttling < THROTTLING:
                                        print(f'ALIM {fixture["fixture_id"]}')
                                        # TODO : Replace mock by api call
                                        # https://api-football-v1.p.rapidapi.com/v2/players/fixture/{fixture}
                                        response = requests.get(f'https://api-football-v1.p.rapidapi.com/v2/players/fixture/{fixture["fixture_id"]}' , headers=headers)
                                        players_data = json.loads(response.content.decode('utf-8'))
                                        print(players_data)
                                        for player in players_data["api"]["players"]:
                                            with open(f'data/fixtures_{followed_league["league_id"]}.json', 'w') as fixtures_json:
                                                tmp = fixtures_data
                                                fixtures_data["api"]["fixtures"][inverse_num]["is_integrated"]=1
                                                json.dump(fixtures_data, fixtures_json)
                                                spamwriter.writerow([followed_league["league_id"], fixture["fixture_id"], fixture["round"] ,player["team_id"], player["team_name"], player["player_id"], player["player_name"], player["position"], player["rating"], player["minutes_played"], player["substitute"], player["shots"]["total"], player["shots"]["on"], player["goals"]["total"],  player["goals"]["conceded"], player["goals"]["assists"], player["passes"]["total"], player["passes"]["key"], player["passes"]["accuracy"], player["tackles"]["total"], player["tackles"]["blocks"], player["tackles"]["interceptions"], player["duels"]["total"], player["duels"]["won"], player["dribbles"]["attempts"], player["dribbles"]["success"], player["dribbles"]["past"], player["fouls"]["drawn"], player["fouls"]["committed"], player["cards"]["yellow"], player["cards"]["red"], player["penalty"]["won"], player["penalty"]["commited"], player["penalty"]["success"], player["penalty"]["missed"], player["penalty"]["saved"]])
                                    else:
                                        break
                                    curr_throttling+=1
                                else:
                                    print(f'ALIM {fixture["fixture_id"]} Already ALIM')
                else:
                    print(f'{followed_league["name"]}_{followed_league["season"]} is not done, use incremental upload instead')
else:
    with open('data/football_data.csv', 'a', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # TODO add league info
        with open('data/followed_leagues.json') as followed_leagues_json:
            followed_leagues_data = json.load(followed_leagues_json)
            for followed_league in followed_leagues_data:
                if followed_league["is_curent"] == 0:
                    if not (os.path.isfile(f'data/fixtures_{followed_league["league_id"]}.json')):
                        pass
                        # https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{followed_league["league_id"]}
                    else:
                        with open(f'data/fixtures_{followed_league["league_id"]}.json', 'r') as fixtures_json:
                            fixtures_data = json.load(fixtures_json)
                            for num, fixture in enumerate(reversed(fixtures_data["api"]["fixtures"]), start=1):
                                inverse_num = len(fixtures_data["api"]["fixtures"]) - num
                                if not 'is_integrated' in fixture:
                                    if curr_throttling < THROTTLING:
                                        print(f'ALIM {fixture["fixture_id"]}')
                                        # TODO : Replace mock by api call
                                        # https://api-football-v1.p.rapidapi.com/v2/players/fixture/{fixture}
                                        response = requests.get(f'https://api-football-v1.p.rapidapi.com/v2/players/fixture/{fixture["fixture_id"]}' , headers=headers)
                                        players_data = json.loads(response.content.decode('utf-8'))
                                        for player in players_data["api"]["players"]:
                                            with open(f'data/fixtures_{followed_league["league_id"]}.json', 'w') as fixtures_json:
                                                tmp = fixtures_data
                                                fixtures_data["api"]["fixtures"][inverse_num]["is_integrated"]=1
                                                json.dump(fixtures_data, fixtures_json)
                                                spamwriter.writerow([followed_league["league_id"], fixture["fixture_id"], fixture["round"] ,player["team_id"], player["team_name"], player["player_id"], player["player_name"], player["position"], player["rating"], player["minutes_played"], player["substitute"], player["shots"]["total"], player["shots"]["on"], player["goals"]["total"],  player["goals"]["conceded"], player["goals"]["assists"], player["passes"]["total"], player["passes"]["key"], player["passes"]["accuracy"], player["tackles"]["total"], player["tackles"]["blocks"], player["tackles"]["interceptions"], player["duels"]["total"], player["duels"]["won"], player["dribbles"]["attempts"], player["dribbles"]["success"], player["dribbles"]["past"], player["fouls"]["drawn"], player["fouls"]["committed"], player["cards"]["yellow"], player["cards"]["red"], player["penalty"]["won"], player["penalty"]["commited"], player["penalty"]["success"], player["penalty"]["missed"], player["penalty"]["saved"]])
                                    else:
                                        break
                                    curr_throttling+=1
                                else:
                                    print(f'ALIM {fixture["fixture_id"]} Already ALIM')
                else:
                    print(f'{followed_league["name"]}_{followed_league["season"]} is not done, use incremental upload instead')
