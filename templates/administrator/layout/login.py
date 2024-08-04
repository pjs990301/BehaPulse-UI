from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def login_layout():
    return html.Div([
        html.Div([
            dbc.Container(
                [
                    html.H2("Hello Again!", className="text-center my-4"),
                    html.P("Welcome Back", className="text-center mb-4"),
                    dbc.Row(
                        dbc.Col([
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText(html.I(className="fas fa-envelope fa-lg")),
                                    dbc.Input(type="email", placeholder="Email Address", className="py-3"),
                                ],
                                className="mb-4 shadow-sm",
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText(html.I(className="fas fa-lock fa-lg")),
                                    dbc.Input(type="password", placeholder="Password", className="py-3"),
                                ],
                                className="mb-4 shadow-sm",
                            ),
                            dbc.Button("Login", color="primary", className="button-login"),
                            html.Div([
                                dbc.Button("회원가입", href="/admin/signup", className="button-secondary"),
                                dbc.Button("비밀번호 찾기", className="button-link"),
                            ], className="button-container")
                        ]),
                    ),
                ],
                className="container text-center"
            )
        ], className="full-screen-container")
    ])
