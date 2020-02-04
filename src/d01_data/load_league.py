from ..d00_utils import utils
import json
import requests
import logging

raw_data_dir = 'data/01_raw/'

def get_leagues(headers):
    logging.info(f'---------- get_all_leagues() ----------')
    utils.flush_file('raw_leagues.json')
    file_name = 'raw_leagues.json'
    with open(f'{raw_data_dir}{file_name}', 'w+') as file_raw_leagues:
        logging.debug(f'Open file {raw_data_dir}{file_name}')
        logging.info('Retrieving all leagues')
        leagues_uri = 'https://api-football-v1.p.rapidapi.com/v2/leagues/'
        response = requests.get(leagues_uri , headers=headers)
        logging.debug(f'Gettting : {leagues_uri}')
        raw_leagues = json.loads(response.content.decode('utf-8'))
        json.dump(raw_leagues, file_raw_leagues)