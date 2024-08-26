from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def find_password_layout():
    return html.Div([
        dbc.Container(
            dbc.Row([
                html.H2("비밀번호 찾기", className="text-center my-4", style={'color': '#4C76FF'}),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(html.I(id='signup-email-icon')),
                        dbc.Input(type="email", placeholder="이메일", className="py-3", id='find-password-email'),
                    ],
                    className="mb-4 password-input-group",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(html.I(id='signup-security-icon')),
                        dbc.Input(type="text", placeholder="질문 (자동으로 기입)", id="security-question",
                                  className="py-3"),
                    ],
                    className="mb-4 password-input-group",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(html.I(id='signup-key-icon')),
                        dbc.Input(type="text", placeholder="답변", id="security-answer", className="py-3"),
                    ],
                    className="mb-4 password-input-group",
                ),
                dbc.Button("비밀번호 찾기", className="mb-3 text-center align-items-center",
                           style={'margin': 'auto', 'width': '60%', 'height': '50px', 'border-radius': '10px',
                                  'display': 'block', 'background-color': '#4C76FF'},
                           id="find-password-button"),

                dbc.Button("돌아가기", href="/admin/", className="button-link w-100"),
                html.Div(id='find-question-message', className='mt-1'),
                html.Div(id='find-password-message', className='mt-1')
            ]), style={'border-radius': '10px'},
            className="p-4 bg-white d-flex flex-column justify-content-center align-items-center shadow-lg m-2"
        )
    ], className="min-vh-100 d-flex align-items-center justify-content-center",
        style={'background-color': 'rgba(49, 97, 255, 0.52)'})