# Basics Requirements
import pathlib
from attr import define
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# assets
srcMap1 = "../assets/ssMapa.png"


# Recall app
from app import app

map = html.Div(
    className="ds4a-map",
    children=[
        html.H5("Mapa"),
        html.Img(src=srcMap1)
    ],
    id="map",
)
