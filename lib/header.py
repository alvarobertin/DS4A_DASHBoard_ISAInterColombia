
import dash
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL, ctx



header= dbc.Row([
                dbc.Col(
                        html.Img(
                                src='assets\ds4a.png',
                                height = "auto",
                                width = '100',), 
                        width={"size": "auto","offset":1},
                        md=0
                ),
                dbc.Col(
                        html.H1('POWER TRANSMISSION LINES RISK DETECTION THROUGH LIDAR DATA ANALYSIS',
                                style = {'font-family':'Trade Gothic LT W01 Oblique','color': 'rgb(0,0,255)','textAlign' : 'center'}), 
                        width={"size": "auto"},
                        md=8
                ),
                dbc.Col(
                        html.Img(
                                src='assets\logo_isa.png',
                                height = '100',
                                #width = 'auto'
                                ), 
                        width={"size": "auto"},
                        md=1
                ),
        ])