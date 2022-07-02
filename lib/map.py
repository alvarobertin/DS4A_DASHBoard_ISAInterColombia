# Basics Requirements
import pathlib
from attr import define
import pydeck
import dash_deck
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

import os
import pandas as pd
import numpy as np

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# assets
srcMap1 = "../assets/ssMapa.png"
DATA_DIR = "../data/"


def test(widget_instance, payload):
    print(widget_instance)

def create(df):

    #df["r"] = np.where(df["Distance"].notnull(), "True", "")

    # if "Distance" in df.columns:
    #     df.loc[df["Distance"].notnull(), 'r'] = 255
    #     df.loc[df["Distance"].notnull(), 'g'] = 0
    #     df.loc[df["Distance"].notnull(), 'b'] = 0

    
    # df = df[["x", "y", "z", "r", "g", "b"]]

    # df = df.sort_values(by=['y', 'x'])

    # if a == 0 and b == 0:
    #     df2 = df[:1000000]
    # else:
    #     df2 = df[a:b]

    target = [df.x.median(), df.y.median(), df.z.median()]

    point_cloud_layer = pydeck.Layer(
        "PointCloudLayer",
        data= df,
        get_position=["x", "y", "z"],
        get_color=["r", "g", "b"],
        #get_normal=[0, 0, 15],
        auto_highlight=True,
        pickable=True,
        point_size=3,
    )
    view_state = pydeck.ViewState(
        target=target,
        rotationOrbit=40,
        zoom=0.5,
        maxZoom=2.5,
        minZoom=-1,
    )
    view = pydeck.View(type="OrbitView", controller=True)

    r = pydeck.Deck(point_cloud_layer, initial_view_state=view_state, views=[view])
    
    r.deck_widget.on_click(test)

    Rjson = r.to_json()

    return Rjson
    
# Recall app
#from app import app


# result = dash_deck.DeckGL(create("LAS-1.csv", 0, 0), id="deck-gl")
tooltip = {
    "html": "<b>{x}</b>, <b>{y}</b>",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}
result = dash_deck.DeckGL({}, id="deck-gl", tooltip=tooltip, enableEvents=['click'])


map = html.Div(
    className="ds4a-map",
    children=[
        #html.H5("Mapa"),
        html.Div(result, id="containerMap")
    ],
    id="map",
)