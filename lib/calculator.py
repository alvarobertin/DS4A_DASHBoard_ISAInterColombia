# Basics Requirements
import pathlib
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Recall app
from app import app
import pyproj


P = pyproj.Proj("+proj=tmerc +ellps=GRS80 +a=6378137.0 +rf=298.257222101 +pm=0 +x_0=5000000.0 +y_0=2000000.0 +lon_0=-73.0 +lat_0=4.0 +units=m +axis=enu ", preserve_units=True)

def calc(x, y):
    a, b = P(x, y, inverse=True) 
    return b, a

calculator = html.Div(
    className="calculator",
    children=[
        dbc.Row([
            dbc.Col(md=1),
            dbc.Col(
                dcc.Markdown('''
            *If you want to geolocate a point, select it in the map. Then, click on map to locate it on Google Maps.* 
            *Zoom In and Zoom out for select the point.*''')),

    ]),
        dbc.Row([
            dbc.Col(md=1),
            dbc.Col(
                dcc.Markdown('''
            X Coordinate
            '''),md=1
            ),
            dbc.Col([
                dcc.Input(id='CordX', type='number', min=2, placeholder="X"),
            ],md=4),
            dbc.Col(
                dcc.Markdown('''
            Y Coordinate
            '''),md=1
            ),
            dbc.Col([
                dcc.Input(id='CordY', type='number', min=2, placeholder="Y")
            ],md=4),
            dbc.Col(md=1),
        ], justify="center"),
        dbc.Row([
            dbc.Col(md=1),
            dbc.Col(
                html.H5(id="Cords"),
                    md=4),
            dbc.Col(
                html.A("Map", id="CordsLink", target="_blank"),
                md=4),
            dbc.Col(md=1),
        ], justify="center")


    ],
    id="calculator",
    
)
