from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def topbar():
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col([dbc.Col(html.H3("Hello Kruluz Utsman", className=""), width="auto"),
                             dbc.Col(html.Small("4:45 pm 19 Jan 2022", className="mb-2"), width="auto"),
                             ]),

                    dbc.Col(html.I(className="fas fa-users"), width="auto")
                ],
                justify="between",
                align="center",

            ),

        ], className="m-4"
    )
