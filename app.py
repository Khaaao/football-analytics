import dash
import src.d07_visualisation.visualize_players
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

df = pd.read_csv('data/06_reporting/players_525.csv', sep = ';', header=0, encoding='utf-8')
players_stats = df.sort_values(by=['round'])
match_played = players_stats['player_id'].value_counts()
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
day = ['Regular Season - 22', 'Regular Season - 21',
       'Regular Season - 15', 'Regular Season - 12',
       'Regular Season - 16', 'Regular Season - 20',
       'Regular Season - 19', 'Regular Season - 18',
       'Regular Season - 17']
jour = [0, 0, 0, 0, 0, 0, 0, 0, 0]

app.layout = html.Div([
    html.Div(
        children=[
            dcc.Dropdown(
                id="players_options",
                options=src.d07_visualisation.visualize_players.build_player_selection(players_stats),
            ),
            src.d07_visualisation.visualize_players.build_banner(),
            html.Div(
                 html.Table([
                    html.Tr([html.Td(['Matchs joués']), html.Td(id='played_match')]),
                ]),
            )
        ]
    ),
    html.Div(
        children=[
            
            html.Div(
                html.Div(
                        [dcc.Graph(id="score_graph")],
                        className="pretty_container seven columns",
                    ),
            )
        ]
    ),
    html.Div(
        children=[
            html.Div(
                html.Div(
                        [dcc.Graph(id="time_graph")],
                        className="pretty_container seven columns",
                    ),
            )
        ]
    )
])

@app.callback(
    Output('played_match', 'children'),
    [Input('players_options', 'value')]
)
def update_main_panel(selected_players):
    return match_played.at[selected_players]

@app.callback(
    Output('score_graph', 'figure'),
    [Input('players_options', 'value')]
)
def update_figure_score_graph(selected_players):
    print(f'{selected_players}')
    return {
        'data': [
            go.Scatter(
                x=players_stats[players_stats['player_id']==selected_players]['round'],
                y=players_stats[players_stats['player_id']==selected_players]['rating'],
                yaxis='y2',
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name='SCORE',
                connectgaps=True
            ),
            go.Bar(
                x=players_stats[players_stats['player_id']==selected_players]['round'],
                y=players_stats[players_stats['player_id']==selected_players]['minutes_played'],
                name='Temps de jeu'
            ),
        ],
        'layout': go.Layout(
            xaxis={'title': 'Journée', 'range': [0, 38], 'dtick': 1},
            yaxis={'title': 'Minutes Played', 'range': [0, 100]},
            yaxis2={'title': 'Score', 'range': [0, 10], 'overlaying': 'y', 'side': 'right'}
        )
    }

@app.callback(
    Output('time_graph', 'figure'),
    [Input('players_options', 'value')]
)
def update_figure_time_graph(selected_players):
    print(players_stats[players_stats['player_id']==selected_players]['minutes_played'])
    return {
        'data': [
            
        ],
        'layout': go.Layout(
            xaxis={'title': 'Journée', 'range': [0, 38], 'dtick': 1},
            yaxis={'title': 'Minutes Played', 'range': [0, 130]}
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)