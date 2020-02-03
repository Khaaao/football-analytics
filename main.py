import runpy
import os
from dotenv import load_dotenv
import src.d01_data.load_league
import src.d01_data.load_fixture
import src.d01_data.control_loading_fixture
import logging
import pickle

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    load_dotenv()
    headers = {'Content-Type': 'application/json', 'x-rapidapi-key': os.getenv("X-RAPIDAPI-KEY")}

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # src.d01_data.load_league.get_all_leagues(headers)
    # src.d01_data.load_fixture.get_fixtures_by_league_id(headers, '525')
    # src.d01_data.load_fixture.handle_fixtures_db('525')
    # src.d01_data.load_fixture.get_fixture_to_load_by_league_id('525')
    src.d01_data.control_loading_fixture.initialize_pickle('525')
    src.d01_data.control_loading_fixture.get_fixture_to_load_by_league_id('525')
    # trottling = os.getenv("TROTTLING")
    # for ()
        
    #     src.d01_data.load_fixture.get_fixture_by_fixture_id(headers, fixture_id)

if __name__ == "__main__":
    main()