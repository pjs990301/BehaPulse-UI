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
            dbc.Row([
                html.H2("회원가입", className="text-center my-4", style={'color': '#4C76FF'}),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(html.I(id='signup-name-icon')),
                        dbc.Input(type="text", placeholder="이름", className="py-3", id='signup-name'),
                    ],
                    className="mb-4 signup-input-group",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(html.I(id='signup-email-icon')),
                        dbc.Input(type="email", placeholder="이메일", className="py-3", id='signup-email'),
                    ],
                    className="mb-4 signup-input-group",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(html.I(id='signup-password-icon')),
                        dbc.Input(type="password", placeholder="비밀번호", className="py-3", id='signup-password'),
                    ],
                    className="mb-4 signup-input-group",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(html.I(id='signup-password-icon')),
                        dbc.Input(type="password", placeholder="비밀번호 확인", className="py-3",
                                  id='signup-password-confirm'),
                    ],
                    className="mb-4 signup-input-group",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(html.I(id='signup-security-icon')),
                        dbc.Input(type="text", placeholder="질문", className="py-3", id="security-question"),
                    ],
                    className="mb-4 signup-input-group",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(html.I(id='signup-key-icon')),
                        dbc.Input(type="text", placeholder="답변", className="py-3", id="security-answer"),
                    ],
                    className="mb-4 signup-input-group",
                ),
                dbc.Button("회원가입", color="primary", className="mb-3 text-center align-items-center",
                           style={'margin': 'auto', 'width': '60%', 'height': '50px', 'border-radius': '10px',
                                  'display': 'block','background-color': '#4C76FF'},
                           id="signup-button"),
                dbc.Button("돌아가기", href="/admin/", className="button-link w-100"),
                html.Div(id='signup-message', className='mt-3'),
            ]), style={'border-radius': '10px'},
            className="p-4 bg-white d-flex flex-column justify-content-center align-items-center shadow-lg m-2"
        )
    ], className="min-vh-100 d-flex align-items-center justify-content-center",
        style={'background-color': 'rgba(49, 97, 255, 0.52)'})