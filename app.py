#from enum import auto
import dash
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
#import os
#import pathlib
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL, ctx
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
# Data
#import math
import numpy as np
import datetime as dt
import pandas as pd
#import json



# Recall app
#from app import app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Dashboard ISA'  

# We need this for function callbacks not present in the app.layout
app.config.suppress_callback_exceptions = True

from lib import map, controlPanel, riskCards, riskHeatMap,calculator,header

app.layout= html.Div(
        style={'backgroundColor': 'rgb(224,222,216)'},
        children= [
############################ Header
        header.header,
        dbc.Row(html.Hr()),
        dbc.Row(
                dbc.Col(
                        dbc.Spinner(children=[
                                dbc.Row([
                                controlPanel.controlPanel,
                                map.map,
                                #html.H6("", id="cords"),
                                calculator.calculator,
                                riskCards.riskCards,
                                dbc.Row(html.Hr()),
                                riskHeatMap.riskHeatMap,
                                ])
                ], 
            fullscreen=True,
            spinnerClassName="spinner"),
            width={'size': 12, 'offset': 0}))
]
)
