from ..d00_utils import utils
import json
import requests
import logging

raw_data_dir = 'data/raw/'

def get_fixtures_by_league_id(headers, league_id):
    logging.info(f'---------- get_fixtures_by_league_id() ----------')
    utils.flush_file(f'data/raw/raw_fixtures_{league_id}.json')
    file_name = f'raw_fixtures_{league_id}.json'
    with open(f'{raw_data_dir}{file_name}', 'w+') as file_raw_fixtures:
        logging.debug(f'Open file {raw_data_dir}{file_name}')
        logging.info('Retrieving all fixtures for one league')
        fixtures_uri = 'https://api-football-v1.p.rapidapi.com/v2/fixtures/league/525'
        response = requests.get(fixtures_uri , headers=headers)
        logging.debug(f'Gettting : {fixtures_uri}')
        raw_fixtures = json.loads(response.content.decode('utf-8'))
        json.dump(raw_fixtures, file_raw_fixtures)         

def get_fixture_by_fixture_id(headers, fixture_id):
    logging.info(f'---------- get_fixture_by_fixture_id() ----------')
    utils.flush_file(f'{raw_data_dir}raw_fixtures_{fixture_id}.json')
    with open(f'data/raw/raw_fixtures_{fixture_id}.json', 'w+') as file_raw_fixture:
        response = requests.get(f'https://api-football-v1.p.rapidapi.com/v2/players/fixture/{fixture_id}' , headers=headers)
        raw_fixture = json.loads(response.content.decode('utf-8'))
        json.dump(raw_fixture, file_raw_fixture)