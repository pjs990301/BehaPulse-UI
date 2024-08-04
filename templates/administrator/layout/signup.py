from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


# Define the layout
def signup_layout():
    return html.Div([
        dbc.Container(
            [
                html.H2("Hello!", className="text-center mt-5"),
                html.P("Sign Up to Get Started", className="text-center mb-4"),
                dbc.Form([
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText(html.I(className="fas fa-user"), className="bg-white border-right-0"),
                            dbc.Input(type="text", placeholder="Full Name", className="border-left-0"),
                        ],
                        className="mb-3 shadow-sm", # Adds shadow for depth
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText(html.I(className="fas fa-envelope"), className="bg-white border-right-0"),
                            dbc.Input(type="email", placeholder="Email Address", className="border-left-0"),
                        ],
                        className="mb-3 shadow-sm",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText(html.I(className="fas fa-lock"), className="bg-white border-right-0"),
                            dbc.Input(type="password", placeholder="Password", className="border-left-0"),
                        ],
                        className="mb-4 shadow-sm",
                    ),
                    dbc.Button("Register", color="primary", className="w-100 shadow-sm"),
                ]),
            ],
            className="my-5 p-3",
            style={"maxWidth": "400px"}
        )
    ], className="bg-light min-vh-100 d-flex align-items-center justify-content-center")