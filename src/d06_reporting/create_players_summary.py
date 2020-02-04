import json
import pickle
import csv

pickle_dir = 'data/pickle_db/'
reporting_dir = 'data/06_reporting/'
raw_data_dir = 'data/01_raw/'
league_id = '525'

def create_players_file():
    with open(f'{reporting_dir}players_{league_id}.csv', 'w', encoding='utf-8', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(
            [
                'player_id',
                'player_name',
                'team_id',
                'team_name',
                'position',
                'round',
                'substitute',
                'minutes_played',
                'goals_conceded',
                'goals_assists',
                'elapsed',
                'rating'
            ]
        )
        fixtures_pickle = open(f'{pickle_dir}league_{league_id}', 'rb')
        fixtures = pickle.load(fixtures_pickle)
        for fixture in fixtures:
            with open(f'{raw_data_dir}raw_fixtures_{league_id}.json', encoding='utf-8') as file_raw_fixtures:
                meta_data_fixtures = json.load(file_raw_fixtures)
                for meta_data_fixture in meta_data_fixtures['api']['fixtures']:
                    if meta_data_fixture['fixture_id'] == fixture['fixture_id']:
                        curr_fixture = meta_data_fixture
                        break
                if fixture['is_loaded'] :
                    with open(f'{raw_data_dir}raw_fixture_{league_id}_{fixture["fixture_id"]}.json', encoding='utf-8') as file_raw_fixture:
                        data_fixture = json.load(file_raw_fixture)
                        for player in data_fixture['api']['players']:
                            spamwriter.writerow(
                                [
                                    player['player_id'],
                                    player['player_name'],
                                    player['team_id'],
                                    player['team_name'],
                                    player['position'],
                                    curr_fixture['round'],
                                    player['substitute'],
                                    player['minutes_played'],
                                    player['goals']['conceded'],
                                    player['goals']['assists'],
                                    curr_fixture['elapsed'],
                                    player['rating']
                                ]
                            )
        fixtures_pickle.close()