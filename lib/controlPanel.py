# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc


#data
import json

# Recall app
from app import app


# Dropdown SELECT LINE

DATA_DIR = "data"
lines_path = os.path.join(DATA_DIR, "lineas.json")
with open(lines_path) as f:
    lines = json.loads(f.read())

lines_dd = dcc.Dropdown(
    id="lines_dd",
    value = lines[list(lines.keys())[0]],
    options=[{"label": key, "value": lines[key]} for key in lines.keys()],
    multi=False,
    placeholder="Select Line"
)

# Dropdown SELECT Feature

DATA_DIR = "data"
features_path = os.path.join(DATA_DIR, "features.json")
with open(features_path) as f:
    features = json.loads(f.read())

features_dd = dcc.Dropdown(
    id="features_dd",
    options=[{"label": key, "value": features[key]} for key in features.keys()],
    multi=True,
    placeholder="Select Feature"
)


controlPanel = html.Div(
    className="ds4a-controlPanel",
    children=[
        html.H5("Control Panel"),
        dbc.Row([
            #izq
            dbc.Col([
                lines_dd
            ]),
            #der
            dbc.Col([
                features_dd
            ]),
        ])
        
    ],
    id="controlPanel"
)
