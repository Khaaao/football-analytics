import json
import pickle
import csv

pickle_dir = 'data/pickle_db/'
reporting_dir = 'data/06_reporting/'
raw_data_dir = 'data/raw/'
league_id = '525'

def create_players_file():
    with open(f'{reporting_dir}players_{league_id}.csv', 'w', encoding='utf-8', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(
            [
                'player_id',
                'player_name',
                'minutes_played'
            ]
        )
        fixtures_pickle = open(f'{pickle_dir}league_{league_id}', 'rb')
        fixtures = pickle.load(fixtures_pickle)
        for fixture in fixtures:
            if fixture['is_loaded'] :
                print(f'{raw_data_dir}raw_fixture_{league_id}_{fixture["fixture_id"]}.json')
                with open(f'{raw_data_dir}raw_fixture_{league_id}_{fixture["fixture_id"]}.json', encoding='utf-8') as file_raw_fixture:
                    data = json.load(file_raw_fixture)
                    for player in data['api']['players']:
                        print(player['player_id'], player['player_name'], player['minutes_played'])
                        spamwriter.writerow(
                            [
                                player['player_id'],
                                player['player_name'],
                                player['minutes_played']
                            ]
                        )
        fixtures_pickle.close()