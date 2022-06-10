# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
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
            #izq
            dbc.Col(
                children=[
                    map.map
                ],
                className="colIzq"
            ),
            #der
            dbc.Col([
                controlPanel.controlPanel,
                riskCards.riskCards,
                riskHeatMap.riskHeatMap,
                riskPointTable.riskPointTable,
            ]),
        ])
    ],
    className="ds4a-app",  # You can also add your own css files by storing them in the assets folder
)



if __name__ == "__main__":
    app.run_server(host="127.0.0.1", port="8050", debug=True)