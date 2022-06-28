#https://dash.gallery/dash-deck-explorer/point-cloud-layer

import pandas as pd
import json
import pydeck
import os
import dash
import dash_deck
from dash import html

def main():
    # archive = "LAS-1.csv"
    #archive = "torres.csv"
    m = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/Line1.csv"))

    df2 = m[1000000*2:1000000*3]

    target = [df2.x.mean(), df2.y.mean(), df2.z.mean()]

    df2 = df2[["x", "y", "z", "r", "g", "b"]]

    point_cloud_layer = pydeck.Layer(
        "PointCloudLayer",
        data=df2,
        get_position=["x", "y", "z"],
        get_color=["r", "g", "b"],
        get_normal=[0, 0, 15],
        auto_highlight=True,
        pickable=True,
        point_size=3,
    )
    view_state = pydeck.ViewState(
        target=target
    )
    view = pydeck.View(type="OrbitView", controller=True)

    r = pydeck.Deck(point_cloud_layer, initial_view_state=view_state, views=[view])
    
   
    Rjson = r.to_json()

    # Save the json file
    # with open('new_file.json', 'w') as f:
    #     json.dump(Rjson, f)

    app = dash.Dash(__name__)
    app.layout = html.Div(
        dash_deck.DeckGL(Rjson, id="deck-gl", style={"background-color": "#add8e6"})
    )


    if __name__ == "__main__":
        app.run_server(debug=True)


main()


