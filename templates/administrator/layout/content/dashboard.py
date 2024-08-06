from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def dashbord_layout():
    return html.Div(
        [
            dbc.Container([
                html.H2("dashbord!", className="my-4"),
                html.P("Sign Up to Get Started", className="mb-4"),
                # Add more content elements as needed
            ],
                className=""
            )
        ], className="mg-0"
    )
