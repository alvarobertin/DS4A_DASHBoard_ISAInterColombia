# Basics Requirements
# https://dash.plotly.com/datatable
import pathlib
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc
from matplotlib.pyplot import table

import os
import pandas as pd

# Recall app
#from app import app

DATA_DIR = "data"
table_path = os.path.join(DATA_DIR, "riskPointTable.csv")
df = pd.read_csv(table_path)


Rtable = dbc.Container([
    dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl')
])


riskPointTable = html.Div(
    className="ds4a-riskPointTable",
    children=[
        html.H5("Specific points with risk"
        #,style = {'font-family':'Trade Gothic LT W01 Oblique','color': 'rgb(0,0,255)' }
        ),
        Rtable,
    ],
    id="riskPointTable",
)
