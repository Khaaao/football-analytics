import runpy
import src.d01_data.load_league
import src.d01_data.load_fixture
import src.d01_data.control_loading_fixture
import src.d06_reporting.create_players_summary
import logging
import pickle

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TROTTLING = 2
league_id = '525'

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Loading MetaData
    # src.d01_data.load_league.get_leagues(headers)

    # Loading Code
    # src.d01_data.load_fixture.get_fixtures_by_league_id(league_id)
    # src.d01_data.control_loading_fixture.initialize_pickle(league_id)
    # for i in range(0, TROTTLING):
    #     fixture_id = src.d01_data.control_loading_fixture.get_fixture_to_load_by_league_id('525')
    #     src.d01_data.load_fixture.get_fixture_by_fixture_id(league_id, fixture_id)

    # Loading Code

    src.d06_reporting.create_players_summary.create_players_file()
    

if __name__ == "__main__":
    main()