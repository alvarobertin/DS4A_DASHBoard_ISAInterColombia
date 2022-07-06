# Basics Requirements
import pathlib
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc
from matplotlib.pyplot import table, text

import os
import pandas as pd

# Recall app
#from app import app

import plotly.graph_objects as go


def create(df):
    if "Risk_Level" in df.columns:
        df2 = df[df["Risk Type"] != "0"][['Risk Type', 'Risk_Level']]
        df2 = df2[df2["Risk Type"] != 0]
        df3 = pd.DataFrame(df2.groupby(['Risk Type', 'Risk_Level']).size()).reset_index()
        df3_p = df3.pivot(index='Risk Type', columns='Risk_Level', values = 0)
        res = df3_p.fillna(0)
        res = res.reindex(columns=["Low Risk", "Medium Risk", "High Risk"])

        dic = {'z': res.values.tolist(),
                'x': res.columns.tolist(),
                'y': res.index.tolist()}

        fig = go.Figure(data=go.Heatmap(dic, type = 'heatmap', colorscale = 'reds'))
    else:
        fig = go.Figure(data=go.Heatmap({}, type = 'heatmap', colorscale = 'reds'))

    fig.update_layout(plot_bgcolor='rgb(224,222,216)',paper_bgcolor='rgb(224,222,216)')
    

    return fig


heatMap = dbc.Container([
    dcc.Graph(
        id="HeatMap",
        figure = go.Figure(data=go.Heatmap({}, type = 'heatmap', colorscale = 'reds'))

        )
])

riskHeatMap = html.Div(
    className="ds4a-riskHeatMap",
    children=[
        dbc.Row([
            dbc.Col(md=1),
            dbc.Col(html.H5("Risk level and risk type"), md=11),
        ]),
        dbc.Row([
            dbc.Col(md=1),
            dbc.Col(heatMap)
        ])
    ],
    id="riskHeatMap",
)
