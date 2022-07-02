# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import pandas as pd
# Dash Bootstrap Components
import dash_bootstrap_components as dbc


#data
import json

# Recall app
#from app import app


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

# Dropdown SELECT LINE section

def secciones(df):
    N = 1000000 # Numero de puntos por seccion 

    n = df.shape[0]/N
    a = 0
    section_options = []
    for i in range(int(n)):
        section_options.append({"label": "Section " + str(i + 1), "value": f"{a} {a + N}"})
        a += N
    return section_options

#section_op = secciones(lines[list(lines.keys())[0]] + ".csv")

section_dd = dcc.Dropdown(
    id="section_dd",
    #value = section_op[0]["value"],
    #options = section_op,
    multi = False,
    placeholder = "Select the section of the line"
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
        html.H2(
            "Control Panel"
            #,style = {'font-family':'Trade Gothic LT W01 Oblique','color': 'rgb(0,0,255)' 
        #,'textAlign' : 'center'}
        ),
        dbc.Row([
            #izq
            dbc.Col([
                lines_dd
            ]),
            #mid
            dbc.Col([
                section_dd
            ]),
            #der
            # dbc.Col([
            #     features_dd
            # ]),
        ])
        
    ],
    id="controlPanel"
)