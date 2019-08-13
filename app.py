import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from pandas.io.json import json_normalize
import pandas as pd
import argparse
import json

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
        id=player_id,
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
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name='GOAL',
                )
            ],
            'layout': go.Layout(
                title={'text': str(matchs_stats[matchs_stats['PLAYER_ID']==player_id]['LASTNAME'].unique()), 'xref': 'paper', 'x': 0},
                xaxis={'title': 'Journée', 'range': [1, 37], 'dtick': 5},
                yaxis={'range': [0, 10], 'dtick': 1}
            )
        }
    )

def generate_for_squad(matchs_stats):
    my_squad = ["437495", "110350", "180299", "193407", "218357", "423151", "227763", "110303", "230718", "88035", "430993", "150670", "42714", "442649", "209874", "216438", "92520"]
    graph = []
    for player in my_squad:
        graph.append(generate_line_graph_by_player_id(matchs_stats, player))

    return graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("player", help="MPG NAME to load config_file")
    parser.add_argument("championchip", help="Specify championchip (FL1 = Ligue 1, PL = PREMIER LEAGUE, PD = Primera Division , FL2 = Ligue 2, SA = Serie A)")
    args = parser.parse_args()

    matchs_stats = normalize_raw_data(pd.read_json(f'data/{args.championchip}_DATA.json'))

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
            html.Div(generate_for_squad(matchs_stats))
        ])
    ])
    app.run_server(debug=True)

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=matchs_stats[matchs_stats['PLAYER_ID']=='37743']['DAY'], y=matchs_stats[matchs_stats['PLAYER_ID']=='37743']['SCORE'],
    #                 mode='lines',
    #                 name=str(matchs_stats[matchs_stats['PLAYER_ID']=='37743']['LASTNAME'])),
    #                 ,
    #             go.Scatter(x=matchs_stats[matchs_stats['PLAYER_ID']=='37743']['DAY'], y=matchs_stats[matchs_stats['PLAYER_ID']=='37743']['GOAL'],
    #                 mode='lines',
    #                 name=str(matchs_stats[matchs_stats['PLAYER_ID']=='37743']['LASTNAME'])))
    # fig.update_xaxes(range=[0, 37])
    # fig.update_yaxes(range=[0, 10])
    # fig.show()

if __name__ == '__main__':
    main()
