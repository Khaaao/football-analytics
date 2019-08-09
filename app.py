import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--player", help="MPG NAME to load config_file")
    parser.add_argument("-c", "--championchip", help="Specify championchip (FL1 = Ligue 1, PL = PREMIER LEAGUE, PD = Primera Division , FL2 = Ligue 2, SA = Serie A)")
    args = parser.parse_args()

    df = pd.DataFrame({'Name': ['Pierre', 'Jean-Louis', 'David'], 'position': ['Attackers', 'Goalkeeper', 'Defender'], 'Score': [[2, 1], [10, 1], [9, 10]]},
                      index = ['437495', '110350', '180299'])

    print(df)

    # app.run_server(debug=True)


if __name__ == '__main__':
    main()
