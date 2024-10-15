from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


# Define the layout
# layout.py
from dash import dcc, html

# def smartthings_layout():
#     return html.Div([
#         dcc.Location(id='url', refresh=False),  # URL tracking component
#         html.Button('Login with OAuth', id='login-button', n_clicks=0),
#         html.Div(id='output-message', children='Click to authenticate'),
#         html.Div(id='token-output'),  # Component to display the token
#         html.Div(id="page-content"),
#     ])

from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def smartthings_layout():
    return html.Div([
        # dcc.Location(id='url', refresh=False),  # URL tracking component
        html.H2("SmartThings 연동 센터", className="text-center my-4", style={'color': '#4C76FF'}),
        html.A(id='token-output', children=' '),  # Component to display the token
        html.Div(id='cards-output', children=' '),  # Component to display the token
        html.Div(id='access-token-output', children='Access Token Output Here:'),
    ])