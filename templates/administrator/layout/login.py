from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Define the layout
# Define the layout
login_layout = html.Div([
    dbc.Container(
        [
            html.H2("Hello Again!", className="text-center my-4"),
            html.P("Welcome Back", className="text-center mb-4"),
            dbc.Row(
                dbc.Col([
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText(html.Img(src="/static/icon_mail.png", height="24px")),  # Removed addon_type
                            dbc.Input(type="email", placeholder="Email Address", className="py-3"),
                        ],
                        className="mb-4",
                        style={"maxWidth": 400}
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText(html.Img(src="/static/icon_lock.png", height="24px")),  # Removed addon_type
                            dbc.Input(type="password", placeholder="Password", className="py-3"),
                        ],
                        className="mb-3",
                        style={"maxWidth": 400}
                    ),
                    dbc.Button("Login", color="primary", className="w-100 mb-3", style={"maxWidth": 400}),
                    dbc.Button("Forgot Password", color="link", className="w-100", style={"maxWidth": 400}),
                ], width=12, className="offset-md-0"),
            ),
        ],
        fluid=True,
        className="py-5",
        style={"height": "100vh", "display": "flex", "flexDirection": "column", "justifyContent": "center"}
    )
], className="bg-white")