# Basics Requirements
import pathlib
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc
from matplotlib.pyplot import table, text

import os
import pandas as pd

# Recall app
from app import app

import plotly.graph_objects as go
feature = [
    "Conductor and Terrain",
    "Vegetation and conductor",
    "Roads and conductor",
    "Conductor and other lines",
    "Conductor and servidumbre",
]

level = [
    "High",
    "Medium",
    "Low",
]

value = [
    [150, 80, 150],
    [20, 50, 104],
    [10, 72, 50],
    [15, 70, 50],
    [50, 90, 100]
]
trace = go.Heatmap(
   x = level,
   y = feature,
   z = value,
   type = 'heatmap',
   colorscale = 'Hot',
   text=value
)
data = [trace]
fig = go.Figure(data = data)

heatMap = dbc.Container([
    dcc.Graph(figure=fig)
])

riskHeatMap = html.Div(
    className="ds4a-riskHeatMap",
    children=[
        html.H5("Risk level and risk type"),
        heatMap,
    ],
    id="riskHeatMap",
)
