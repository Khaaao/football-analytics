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

app.layout = html.Div([
    html.Div(
        children=[
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
            dcc.Dropdown(
                id="players_options",
                options=src.d07_visualisation.visualize_players.build_player_selection(players_stats),
            ),
            html.Div(
                html.Div(
                        [dcc.Graph(id="main_graph")],
                        className="pretty_container seven columns",
                    ),
            )
        ]
    ),
    html.Div(
        className="main-panel"
    )
])

@app.callback(
    Output('played_match', 'children'),
    [Input('players_options', 'value')]
)
def update_main_panel(selected_players):
    return match_played.at[selected_players]

@app.callback(
    Output('main_graph', 'figure'),
    [Input('players_options', 'value')]
)
def update_figure(selected_players):
    print(f'{selected_players}')
    return {
        'data': [
            go.Scatter(
                x=players_stats['round'].unique(),
                y=players_stats[players_stats['player_id']==selected_players]['rating'],
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name='SCORE',
                connectgaps=True
                ),
        ],
        'layout': go.Layout(
            xaxis={'title': 'Journée', 'range': [0, 38], 'dtick': 1},
            yaxis={'title': 'Score', 'range': [0, 10]}
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)