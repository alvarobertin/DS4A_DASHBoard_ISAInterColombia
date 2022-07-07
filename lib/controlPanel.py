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


controlPanel = html.Div(
    className="ds4a-controlPanel",
    children=[
        dbc.Row([
            dbc.Col(md=1),
            dbc.Col(html.H2(
                     "Control Panel"
            ), md=11),
        ]),
        dbc.Row([
            dbc.Col(md=1),
            dbc.Col(
               dcc.Markdown('''
                *Please select one power line and one segment to visualize it*
                '''
                ), md=11
            )
        ]),
        
        dbc.Row([
            dbc.Col(md=1),
            #izq
            dbc.Col([
                lines_dd
            ],
            md=5),
            #der
            dbc.Col([
                section_dd
            ],md=5),
            dbc.Col(md=1),
    
        ],
        justify="around")
        
    ],
    id="controlPanel"
)