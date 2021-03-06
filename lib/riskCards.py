# Basics Requirements
import pathlib
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Recall app
#from app import app

riskCards = html.Div(
    className="ds4a-riskCards",
    children=[
        dbc.Row([
            #Total
            dbc.Col(
                children=[
                    html.H6("0", id="total_card"),
                    html.H6("Total Risks")
                ],
                id="riskCardTotal",
                className="riskCard"
            ),
            #High
            dbc.Col(
                children=[
                    html.H6("0", id="high_card"),
                    html.H6("High Risks")
                ],
                id="riskCardHigh",
                className="riskCard"
            ),
            #Medium
            dbc.Col(
                children=[
                    html.H6("0", id="medium_card"),
                    html.H6("Medium Risks")
                ],
                id="riskCardMedium",
                className="riskCard"
            ),
            #Low
            dbc.Col(
                children=[
                    html.H6("0", id="low_card"),
                    html.H6("Low Risks")
                ],
                id="riskCardLow",
                className="riskCard"
            ),
        ])
    ],
    id="riskCards",
)
