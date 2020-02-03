from ..d00_utils import utils
import json
import requests
import logging
import pickle
from dotenv import load_dotenv

raw_data_dir = 'data/raw/'
pickle_dir = 'data/pickle_db/'

load_dotenv()

headers = {'Content-Type': 'application/json', 'x-rapidapi-key': os.getenv("X-RAPIDAPI-KEY")}

def get_fixtures_by_league_id(league_id):
    logging.info(f'---------- get_fixtures_by_league_id() ----------')
    utils.flush_file(f'data/raw/raw_fixtures_{league_id}.json')
    file_name = f'raw_fixtures_{league_id}.json'
    with open(f'{raw_data_dir}{file_name}', 'w+') as file_raw_fixtures:
        logging.debug(f'Open file {raw_data_dir}{file_name}')
        logging.info('Retrieving all fixtures for one league')
        fixtures_uri = 'https://api-football-v1.p.rapidapi.com/v2/fixtures/league/525'
        response = requests.get(fixtures_uri , headers)
        logging.debug(f'Gettting : {fixtures_uri}')
        raw_fixtures = json.loads(response.content.decode('utf-8'))
        json.dump(raw_fixtures, file_raw_fixtures)         

def get_fixture_by_fixture_id(league_id, fixture_id):
    logging.info(f'---------- get_fixture_by_fixture_id({league_id, fixture_id}) ----------')
    utils.flush_file(f'{raw_data_dir}raw_fixture_{fixture_id}.json')
    with open(f'{raw_data_dir}raw_fixture_{league_id}_{fixture_id}.json', 'w+') as file_raw_fixture:
        response = requests.get(f'https://api-football-v1.p.rapidapi.com/v2/players/fixture/{fixture_id}' , headers)
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