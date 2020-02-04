import dash_core_components as dcc
import dash_html_components as html
import pandas as pd



from pandas.io.json import json_normalize
import argparse
import json

def build_banner() :
    return html.Div(
        className="banner",
        children=[
            html.H1("Football Data Analytics"),
        ],
    )

def build_player_selection(players_stats) :
    return [
        {"label": str(players_stats[players_stats['player_id']==player_id]['player_name'].unique()), "value": player_id}
        for player_id in players_stats["player_id"]
    ]