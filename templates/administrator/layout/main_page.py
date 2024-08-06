from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from .sidebar import sidebar
from .topbar import topbar


def main_layout():
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(sidebar(), width=2, style={'border-right': '1px solid #ccc'},
                    className="d-flex flex-column justify-content-between vh-100"),
            dbc.Col([
                topbar(),
                html.Hr(),
                html.Div(
                    id="page-content",
                    style={"height": "100%", "overflow-y": "hidden"}
                )
            ], width=10, className="d-flex flex-column justify-content-between vh-100 p-0")
        ])
    ], fluid=True, className="vh-100")

    return layout
