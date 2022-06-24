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
from lib import title, map, controlPanel, riskCards, riskPointTable, riskHeatMap

# PLACE THE COMPONENTS IN THE LAYOUT
app.layout = html.Div(
    [
        title.title,
        dbc.Row([
            controlPanel.controlPanel,
            map.map,
            riskCards.riskCards,
            riskHeatMap.riskHeatMap,
            riskPointTable.riskPointTable,
        ])
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