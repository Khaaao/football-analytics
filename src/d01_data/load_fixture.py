from ..d00_utils import utils
import json
import requests
import logging
import pickle
import os

raw_data_dir = 'data/01_raw/'
pickle_dir = 'data/pickle_db/'

def get_fixtures_by_league_id(headers, league_id):
    logging.info(f'---------- get_fixtures_by_league_id() ----------')
    utils.flush_file(f'data/raw/raw_fixtures_{league_id}.json')
    file_name = f'raw_fixtures_{league_id}.json'
    with open(f'{raw_data_dir}{file_name}', 'w+') as file_raw_fixtures:
        logging.info('Retrieving all fixtures for one league')
        fixtures_uri = 'https://api-football-v1.p.rapidapi.com/v2/fixtures/league/525'
        print(headers)
        response = requests.get(fixtures_uri , headers=headers)
        raw_fixtures = json.loads(response.content.decode('utf-8'))
        json.dump(raw_fixtures, file_raw_fixtures)         

def get_fixture_by_fixture_id(headers, league_id, fixture_id):
    logging.info(f'---------- get_fixture_by_fixture_id({league_id, fixture_id}) ----------')
    utils.flush_file(f'{raw_data_dir}raw_fixture_{fixture_id}.json')
    with open(f'{raw_data_dir}raw_fixture_{league_id}_{fixture_id}.json', 'w+') as file_raw_fixture:
        response = requests.get(f'https://api-football-v1.p.rapidapi.com/v2/players/fixture/{fixture_id}' , headers=headers)
        raw_fixture = json.loads(response.content.decode('utf-8'))
        json.dump(raw_fixture, file_raw_fixture)

    fixtures_pickle = open(f'{pickle_dir}league_{league_id}', 'rb')
    fixtures = pickle.load(fixtures_pickle)
    for fixture in fixtures :
        if (fixture['fixture_id'] == fixture_id) :
            logging.info(f'{fixture_id} is loaded.')
            fixture['is_loaded'] = True
            break
    fixtures_pickle.close()
    fixtures_pickle_write = open(f'{pickle_dir}league_{league_id}', 'wb')
    pickle.dump(fixtures, fixtures_pickle_write)
    fixtures_pickle_write.close()