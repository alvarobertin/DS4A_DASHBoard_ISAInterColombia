#https://dash.gallery/dash-deck-explorer/point-cloud-layer

import pandas as pd
import json
import pydeck
import os
import dash
import dash_deck
from dash import html
from dash.dependencies import Input, Output

def main():
    # archive = "LAS-1.csv"
    #archive = "torres.csv"
    m = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/LAS-1.csv"))

    df2 = m[0:10000]

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

    tooltip = {
    "html": "<b>{x}</b>, <b>{y}</b>",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
    }

    app.layout = html.Div([
            dash_deck.DeckGL(Rjson, id="deck-gl", style={"background-color": "#add8e6"}, tooltip=tooltip,enableEvents=True),
            html.Div(
                children=[
                    html.P("clickInfo"),
                    html.Pre(id="click-info-json-output"),
                    html.P("clickEvent"),
                    html.Pre(id="click-event-json-output"),
                ],
            ),
        ]
    )


    def assign_callback(app, out, event):
        @app.callback(Output(f"{out}-json-output", "children"), [Input("deck-gl", event)])
        def dump_json(data):
            if data != None:
                print(data['object'])
            return json.dumps(data, indent=2)


    assign_callback(app, "click-info", "clickInfo")
    # assign_callback(app, "click-event", "clickEvent")

    if __name__ == "__main__":
        app.run_server(debug=True)


main()


