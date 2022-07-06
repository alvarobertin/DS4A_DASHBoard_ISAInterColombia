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

from lib import map, controlPanel, riskCards, riskPointTable, riskHeatMap,calculator,header

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
                                #riskPointTable.riskPointTable,
                                ])
                ], 
            fullscreen=True,
            spinnerClassName="spinner"),
            width={'size': 12, 'offset': 0}))
]
)

###############################################
#
#           APP INTERACTIVITY:
#
###############################################

# anterior = ""
# @app.callback(
#     [
#         Output("deck-gl", "data"),
#         Output("section_dd", "options"),
#         Output("section_dd", "value"),
#     ],
#     [
#         Input("lines_dd", "value"),
#         Input("section_dd", "value"),
#     ],
# )
# def make_line_plot(lines_dd, section_dd):
#     if section_dd == None:
#         a, b = 0, 0
#     else:
#         s = section_dd.split()
#         a = int(s[0])
#         b = int(s[1])

#     map_data = map.create(lines_dd + ".csv", a, b)
#     # Esto se debe cambiar para no abrir tantas veces un csv 
#     section_options = controlPanel.secciones(lines_dd + ".csv")

#     if ctx.triggered_id == "section_dd":
#         anterior = section_dd
#     else:
#         anterior = section_options[0]["value"]
#     return [map_data, section_options, anterior]


# if __name__ == "__main__":
#     app.run_server(host="127.0.0.1", port="8051", debug=True)