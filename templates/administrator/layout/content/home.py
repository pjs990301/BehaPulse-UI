from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def home_layout():
    return html.Div(
        dbc.Container([
            # html.H2("Home!", className="my-4"),
            # html.P("Sign Up to Get Started", className="mb-4"),
            # Add more content elements as needed
            dbc.Row(
                [
                    dbc.Col([html.I(className="fas fa-house-user fa-lg m-3"), "즐겨찾기"],
                            style={"font-size": "1.5em"},
                            ),
                    dbc.Col(dbc.Button("Edit Tutor", color="primary", className="mr-1"), width={"size": 3, "offset": 2},
                            align="end")
                ],
            )
        ],
            className="mt-5 mx-3")
    )
