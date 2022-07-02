# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL, ctx
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

# Recall app
from app import app

DATA_DIR = "data"

###########################################################
#
#           APP LAYOUT:
#
###########################################################


# LOAD THE DIFFERENT FILES
from lib import title, map, controlPanel, riskCards, riskPointTable, riskHeatMap#, calculator

# PLACE THE COMPONENTS IN THE LAYOUT
app.layout = html.Div(
    children=[
        title.title,
        dbc.Row(dbc.Col(
            dbc.Spinner(
            children=[
                dbc.Row([
                    controlPanel.controlPanel,
                    map.map,
                    html.H6("", id="cords"),
                    #calculator.calculator,
                    riskCards.riskCards,
                    riskHeatMap.riskHeatMap,
                    riskPointTable.riskPointTable,],
                )], 
            fullscreen=True,
            spinnerClassName="spinner"),
            width={'size': 12, 'offset': 0}),
        ),
    ],
    className="ds4a-app",  # You can also add your own css files by storing them in the assets folder
)


###############################################
#
#           APP INTERACTIVITY:
#
###############################################

anterior = ""
@app.callback(
    [
        Output("deck-gl", "data"),
        Output("section_dd", "options"),
        Output("section_dd", "value"),
        Output("total_card", "children"),
        Output("high_card", "children"),
        Output("medium_card", "children"),
        Output("low_card", "children"),
        Output("HeatMap", "figure"),
    ],
    [
        Input("lines_dd", "value"),
        Input("section_dd", "value"),
    ],
)
def make_line_plot(lines_dd, section_dd):
    print("callback")

    csv_path = os.path.join(DATA_DIR, lines_dd + ".csv")
    
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), csv_path))

    section_options = controlPanel.secciones(df)

    if section_dd == None:
        a, b = 0, 0
    else:
        s = section_dd.split()
        a = int(s[0])
        b = int(s[1])

    df = df.sort_values(by=['y', 'x'])

    if a == 0 and b == 0:
        df = df[:1000000]
    else:
        df = df[a:b]

    map_data = map.create(df[["x", "y", "z", "r", "g", "b"]])
 

    if ctx.triggered_id == "section_dd":
        anterior = section_dd
    else:
        anterior = section_options[0]["value"]

    nTotal = 0
    nHigh = 0
    nMedium = 0
    nLow = 0

    if "Risk_Level" in df.columns:
        nHigh = df[df['Risk_Level'] == "High Risk"]['Risk_Level'].count()
        nMedium = df[df['Risk_Level'] == "Medium Risk"]['Risk_Level'].count()
        nLow = df[df['Risk_Level'] == "Low Risk"]['Risk_Level'].count()
        nTotal = nHigh + nMedium + nLow

    
    HeatMap = riskHeatMap.create(df)

    return [map_data, section_options, anterior, nTotal, nHigh, nMedium, nLow, HeatMap]

@app.callback(
    [
        Output("CordX", "value"),
        Output("CordY", "value")
    ], 
    [
        Input("deck-gl", "clickInfo")
    ]
)
def dump_json(data):
    value = ""
    x = None
    y = None
    if data != None:
        if data['object'] != None:
            #print(data['object'])
            x = (data['object']['x'])
            y = (data['object']['y'])
            # value = f"{data['object']['x']} {data['object']['y']}"
    return [x, y]


@app.callback(
    [
        Output("deck-gl", "data"),
        Output("section_dd", "options"),
        Output("section_dd", "value"),
    ],
    [
        Input("lines_dd", "value"),
        Input("section_dd", "value"),
    ],
)
def make_line_plot(lines_dd, section_dd):
    if section_dd == None:
        a, b = 0, 0
    else:
        s = section_dd.split()
        a = int(s[0])
        b = int(s[1])

    map_data = map.create(lines_dd + ".csv", a, b)
    # Esto se debe cambiar para no abrir tantas veces un csv 
    section_options = controlPanel.secciones(lines_dd + ".csv")

    if ctx.triggered_id == "section_dd":
        anterior = section_dd
    else:
        anterior = section_options[0]["value"]
    return [map_data, section_options, anterior]

if __name__ == "__main__":
    app.run_server(host="127.0.0.1", port="8050", debug=True)