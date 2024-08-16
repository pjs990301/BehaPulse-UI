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
            dbc.Row(
                dbc.Col(
                    [
                        html.H2("Hello!", className="text-center my-4"),
                        html.P("Sign Up to Get Started", className="text-center mb-4"),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(html.I(className="fas fa-user fa-lg", style={"color": "#6c757d"})),
                                dbc.Input(type="text", placeholder="이름", className="py-3", id='signup-name'),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    html.I(className="fas fa-envelope fa-lg", style={"color": "#6c757d"})),
                                dbc.Input(type="email", placeholder="이메일", className="py-3", id='signup-email'),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(html.I(className="fas fa-lock fa-lg", style={"color": "#6c757d"})),
                                dbc.Input(type="password", placeholder="비밀번호", className="py-3", id='signup-password'),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(html.I(className="fas fa-lock fa-lg", style={"color": "#6c757d"})),
                                dbc.Input(type="password", placeholder="비밀번호 확인", className="py-3",
                                          id='signup-password-confirm'),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    html.I(className="fas fa-question fa-lg", style={"color": "#6c757d"})),
                                dbc.Input(type="text", placeholder="질문", className="py-3", id="security-question"),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(html.I(className="fas fa-key fa-lg", style={"color": "#6c757d"})),
                                dbc.Input(type="text", placeholder="답변", className="py-3", id="security-answer"),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.Button("회원가입", color="primary",
                                   className="mb-3 d-block text-center align-items-center w-100", id="signup-button"),
                        dbc.Button("돌아가기", href="/admin/", className="button-link w-100"),
                        html.Div(id='signup-message', className='mt-3'),
                    ],

                    xs=12, sm=12, md=8, lg=6, xl=4, style={'margin': 'auto'},
                    className="p-4 shadow-sl rounded bg-white"
                )
            ), fluid=True)
    ], className="bg-light min-vh-100 d-flex align-items-center justify-content-center")
