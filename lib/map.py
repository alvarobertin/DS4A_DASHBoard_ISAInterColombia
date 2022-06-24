# Basics Requirements
import pathlib
from attr import define
import pydeck
import dash_deck
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

import os
import pandas as pd

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# assets
srcMap1 = "../assets/ssMapa.png"
DATA_DIR = "../data/"

def create(archive, a, b):
    csv_path = os.path.join(DATA_DIR, archive)
    
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), csv_path))

    if a == 0 and b == 0:
        df2 = df[:1000000]
    else:
        df2 = df[a:b]

    target = [df2.x.median(), df2.y.median(), df2.z.median()]

    point_cloud_layer = pydeck.Layer(
        "PointCloudLayer",
        data=df2,
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
    
   
    Rjson = r.to_json()

    return Rjson
    
# Recall app
from app import app


result = dash_deck.DeckGL(create("LAS-1.csv", 0, 0), id="deck-gl")

map = html.Div(
    className="ds4a-map",
    children=[
        html.H5("Mapa"),
        html.Div(result, id="containerMap")
    ],
    id="map",
)
