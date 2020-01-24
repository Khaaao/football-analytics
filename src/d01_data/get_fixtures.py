import os
from dotenv import load_dotenv
from ..d00_utils import utils
import json
import requests

load_dotenv()
headers = {'Content-Type': 'application/json', 'x-rapidapi-key': os.getenv("X-RAPIDAPI-KEY")}
utils.refresh_raw_input('raw_fixtures_525.json')

with open('data/raw/raw_fixtures_525.json', 'w+') as file_raw_fixtures:
    response = requests.get('https://api-football-v1.p.rapidapi.com/v2/fixtures/league/525' , headers=headers)
    raw_fixtures = json.loads(response.content.decode('utf-8'))
    json.dump(raw_fixtures, file_raw_fixtures)