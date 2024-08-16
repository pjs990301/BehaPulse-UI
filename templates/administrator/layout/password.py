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
                                    html.I(className="fas fa-envelope fa-lg", style={"color": "#6c757d"})),
                                dbc.Input(type="email", placeholder="이메일", className="py-3", id='find-password-email'),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    html.I(className="fas fa-question fa-lg", style={"color": "#6c757d"})),
                                dbc.Input(type="text", placeholder="질문 (자동으로 기입)", id="security-question",
                                          className="py-3"),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(html.I(className="fas fa-key fa-lg", style={"color": "#6c757d"})),
                                dbc.Input(type="text", placeholder="답변", id="security-answer", className="py-3"),
                            ],
                            className="mb-4 shadow-sm",
                        ),
                        dbc.Button("비밀번호 찾기", color="primary",
                                   className="mb-3 d-block text-center align-items-center w-100",
                                   id="find-password-button"),

                        dbc.Button("돌아가기", href="/admin/", className="button-link w-100"),
                        html.Div(id='find-question-message', className='mt-3'),
                        html.Div(id='find-password-message', className='mt-3')
                    ],
                    xs=12, sm=12, md=8, lg=6, xl=4, style={'margin': 'auto'},
                    className="p-4 shadow-sm rounded bg-white"
                )
            ), fluid=True)
    ], className="bg-light min-vh-100 d-flex align-items-center justify-content-center")
