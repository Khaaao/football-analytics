import requests
import logging
import pickle
import os
import json

pickle_dir = 'data/pickle_db/'
raw_data_dir = 'data/01_raw/'

def initialize_pickle(league_id):
    logging.info(f'---------- initialize_pickle({league_id}) ----------')
    if (os.path.isfile(f'{pickle_dir}league_{league_id}')):
        logging.info(f'File already exist')
    else:
        with open(f'{raw_data_dir}raw_fixtures_{league_id}.json') as json_file:
            fixtures = []
            logging.info(f'Creating Pickle')
            fixtures_pickle_write = open(f'{pickle_dir}league_{league_id}', 'wb')
            data = json.load(json_file)
            for fixture in data['api']['fixtures']:
                tmp_object = {
                    'fixture_id': fixture['fixture_id'],
                    'event_date': fixture['event_date'],
                    'status': fixture['status'],
                    'is_loaded': False
                }
                fixtures.append(tmp_object)
            fixtures.reverse()
            pickle.dump(fixtures, fixtures_pickle_write)
            fixtures_pickle_write.close()

def get_fixture_to_load_by_league_id(league_id):
    logging.info(f'---------- get_fixture_to_load_by_league_id({league_id}) ----------')
    # fixtures_pickle = pickle.load(open(f'{pickle_dir}league_{league_id}', 'rb'))
    fixtures_pickle = open(f'{pickle_dir}league_{league_id}', 'rb')
    fixtures = pickle.load(fixtures_pickle)
    for fixture in fixtures:
        # Si le match est terminée et non télécharger
        if(fixture['status'] == 'Match Finished' and not fixture['is_loaded']):
            return fixture['fixture_id']
    fixtures_pickle.close()