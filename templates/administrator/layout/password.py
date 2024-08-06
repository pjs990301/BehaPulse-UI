from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def find_password_layout():
    return html.Div([
        dbc.Container(
            dbc.Row(
                dbc.Col(
                    [
                        html.H2("Hello!", className="text-center my-4"),
                        html.P("Enter your email to reset your password", className="text-center mb-4"),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    html.I(className="fas fa-envelope fa-lg", style={"color": "#6c757d"}),
                                    className="bg-white border-right-0"),
                                dbc.Input(type="email", placeholder="이메일", className="py-3"),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    html.I(className="fas fa-question fa-lg", style={"color": "#6c757d"}),
                                    className="bg-white border-right-0"),
                                dbc.Input(type="text", placeholder="질문", id="security-question", className="py-3"),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(html.I(className="fas fa-key fa-lg", style={"color": "#6c757d"}),
                                                   className="bg-white border-right-0"),
                                dbc.Input(type="text", placeholder="답변", id="security-answer", className="py-3"),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.Button("비밀번호 찾기", color="primary",
                                   className="mb-3 d-block text-center align-items-center w-100"),

                        dbc.Button("돌아가기", href="/admin/", className="button-link w-100"),
                        # dbc.Button("회원가입", href="/admin/signup", className="button-link"),

                    ],
                    xs=12, sm=12, md=8, lg=6, xl=4, style={'margin': 'auto'},
                    className="p-4 shadow-sm rounded bg-white"
                )
            ), fluid=True)
    ], className="bg-light min-vh-100 d-flex align-items-center justify-content-center")
