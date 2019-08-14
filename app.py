import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pandas.io.json import json_normalize
import pandas as pd
import argparse
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def was_on_field(player_data):
    ''' Basic function, return if player played '''
    if player_data["info"]["mins_played"] == 0:
        return False
    else:
        return True

def generate_row(day, match_id, player_data, club):
    ''' Format new row for append in DataFrame '''
    if was_on_field(player_data):
        row = pd.Series([day + 1, match_id, player_data["info"]["idplayer"], player_data["info"]["lastname"], player_data["info"]["position"], club, player_data["info"]['goals'], player_data["info"]["note_final_2015"], player_data["info"]["mins_played"]], index=['DAY', 'MATCH_ID', 'PLAYER_ID', 'LASTNAME', 'POSITION', 'CLUB', 'GOAL', 'SCORE', 'MIN_PLAYED'])
    else:
        row = pd.Series([day + 1, match_id, player_data["info"]["idplayer"],player_data["info"]["lastname"], player_data["info"]["position"], club, None, None, None], index=['DAY', 'MATCH_ID', 'PLAYER_ID', 'LASTNAME', 'POSITION', 'CLUB', 'GOAL', 'SCORE', 'MIN_PLAYED'])
    return row

def normalize_raw_data(raw_data):
    ''' Format row data '''
    matchs_stats = pd.DataFrame()
    for day,val in raw_data.iterrows():
        for match in val["matchs"]:
            for player_key, player_data in match["Home"]["players"].items():
                row_to_insert = generate_row(day, match["id"], player_data, match["Home"]["club"])
                matchs_stats = matchs_stats.append(row_to_insert, ignore_index=True)
            for key, player_data in match["Away"]["players"].items():
                row_to_insert = generate_row(day, match["id"], player_data, match["Away"]["club"])
                matchs_stats = matchs_stats.append(row_to_insert, ignore_index=True)
    return matchs_stats

def generate_line_graph_by_player_id(matchs_stats, player_id):
    return dcc.Graph(
        id=f'{player_id}_first_chart',
        figure={
            'data': [
                go.Scatter(
                    x=matchs_stats[matchs_stats['PLAYER_ID']==player_id]['DAY'],
                    y=matchs_stats[matchs_stats['PLAYER_ID']==player_id]['SCORE'],
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name='SCORE',
                ),
                go.Scatter(
                    x=matchs_stats[matchs_stats['PLAYER_ID']==player_id]['DAY'],
                    y=matchs_stats[matchs_stats['PLAYER_ID']==player_id]['GOAL'],
                    mode='markers',
                    name='GOAL',
                )
            ],
            'layout': go.Layout(
                title={'text': str(matchs_stats[matchs_stats['PLAYER_ID']==player_id]['LASTNAME'].unique()), 'xref': 'paper', 'x': 0},
                xaxis={'title': 'Journée', 'range': [0, 38], 'dtick': 5},
                yaxis={'range': [0, 10], 'dtick': 1}
            )
        }
    )

def generate_bar_graph_by_player_id(matchs_stats, player_id):
    return dcc.Graph(
        id=f'{player_id}_second_chart',
        figure={
            'data': [
                go.Bar(
                    x=matchs_stats[matchs_stats['PLAYER_ID']==player_id]['DAY'],
                    y=matchs_stats[matchs_stats['PLAYER_ID']==player_id]['MIN_PLAYED'],
                    name='MIN_PLAYED',
                )
            ],
            'layout': go.Layout(
                title={'text': str(matchs_stats[matchs_stats['PLAYER_ID']==player_id]['LASTNAME'].unique()), 'xref': 'paper', 'x': 0},
                xaxis={'title': 'Journée', 'range': [0, 38], 'dtick': 5},
                yaxis={'title': 'Minutes played', 'dtick': 20}
            )
        }
    )

def generate_for_squad(matchs_stats):
    my_squad = ["437495", "110350", "180299", "193407", "218357", "423151", "227763", "110303", "230718", "88035", "430993", "150670", "42714", "442649", "209874", "216438", "92520"]
    graph = []
    for player in my_squad:
        graph.append(generate_line_graph_by_player_id(matchs_stats, player))
        graph.append(generate_bar_graph_by_player_id(matchs_stats, player))
    return graph

def generate_dropdown_options(matchs_stats):
    return [
        {"label": str(matchs_stats[matchs_stats['PLAYER_ID']==player_id]['LASTNAME'].unique()), "value": str(player_id)}
        for player_id in matchs_stats["PLAYER_ID"]
    ]


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server

# Load argument
parser = argparse.ArgumentParser()
parser.add_argument("player", help="MPG NAME to load config_file")
parser.add_argument("championchip", help="Specify championchip (FL1 = Ligue 1, PL = PREMIER LEAGUE, PD = Primera Division , FL2 = Ligue 2, SA = Serie A)")
args = parser.parse_args()

# Load data
# matchs_stats = normalize_raw_data(pd.read_json(f'data/{args.championchip}_DATA.json'))
matchs_stats = pd.read_csv('data/football_data.csv')

# Create app layout
app.layout = html.Div(children=[
    html.Div([
        html.Div(
            [
                html.H3(
                    "In-Depth Player Analysis",
                    style={"margin-bottom": "0px"},
                ),
            ],
            className="one-half column",
            id="title",
        ),
        html.Div(
            dcc.Dropdown(
                id="players_options",
                options=generate_dropdown_options(matchs_stats),
            )
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="goal_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"}
    )
])

@app.callback(
    Output('goal_graph', 'figure'),
    [Input('players_options', 'value')]
)
def update_figure(selected_players):
    return {
        'data': [
            go.Bar(
                x=matchs_stats[matchs_stats['PLAYER_ID']==selected_players]['DAY'],
                y=matchs_stats[matchs_stats['PLAYER_ID']==selected_players]['GOAL'],
                name='GOAL',
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Day', 'range': [0, 38], 'dtick': 5},
            yaxis={'title': 'Goal', 'range': [0, 5], 'dtick': 1}
        )
}

@app.callback(
    Output('main_graph', 'figure'),
    [Input('players_options', 'value')]
)
def update_figure(selected_players):
    return {
        'data': [
            go.Scatter(
                x=matchs_stats[matchs_stats['PLAYER_ID']==selected_players]['DAY'],
                y=matchs_stats[matchs_stats['PLAYER_ID']==selected_players]['SCORE'],
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                    name='SCORE',
                )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Day', 'range': [0, 38], 'dtick': 5},
            yaxis={'title': 'Score', 'range': [0, 10], 'dtick': 1}
        )
}

if __name__ == '__main__':
    app.run_server(debug=True)
