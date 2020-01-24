import os
from dotenv import load_dotenv
from ..d00_utils import utils
import json
import requests

load_dotenv()
headers = {'Content-Type': 'application/json', 'x-rapidapi-key': os.getenv("X-RAPIDAPI-KEY")}
utils.refresh_raw_input('raw_leagues.json')

with open('data/raw/raw_leagues.json', 'w+') as file_raw_leagues:
    response = requests.get('https://api-football-v1.p.rapidapi.com/v2/leagues/' , headers=headers)
    raw_leagues = json.loads(response.content.decode('utf-8'))
    json.dump(raw_leagues, file_raw_leagues)