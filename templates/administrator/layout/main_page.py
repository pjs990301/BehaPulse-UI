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
            dbc.Col(sidebar(), width=1, style={'border-right': '2px solid #ccc'},
                    className="d-flex flex-column justify-content-between vh-100"),
            dbc.Col([
                topbar(),
                html.Div(
                    id="page-content",
                    style={"background-color": "rgba(82, 128, 255, 0.08)", "height": "100%", "overflow-y": "hidden"}
                )
            ], width=11, className="d-flex flex-column justify-content-between vh-100 p-0")
        ])
    ], fluid=True, className="vh-100")

    return layout
