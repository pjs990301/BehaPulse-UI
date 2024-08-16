from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def login_layout():
    return html.Div([
        dbc.Container([
            dbc.Row([
                html.Img(src="assets/img/logo.png", style={'width': '150px'}),
            ]),
            dbc.Row(
                dbc.Col([
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText(html.I(className="fas fa-envelope fa-lg", style={"color": "#6c757d"})),
                            dbc.Input(type="email", placeholder="이메일", className="py-3", id='login-email'),
                        ],
                        className="mb-4 shadow-sm",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText(html.I(className="fas fa-lock fa-lg", style={"color": "#6c757d"})),
                            dbc.Input(type="password", placeholder="비밀번호", className="py-3", id='login-password'),
                        ],
                        className="mb-4 shadow-sm",
                    ),
                    dbc.Button("로그인", color="primary", className="mb-3 d-block text-center align-items-center w-100",
                               # href="/admin/main"),
                               id="login-button"),
                    dbc.Button("회원가입", href="/admin/signup", className="button-link"),
                    dbc.Button("비밀번호 찾기", href='/admin/password', className="button-link"),
                    html.Div(id='login-message', className='mt-3')
                ],
                    className="p-4 shadow-sm bg-white", style={'margin': 'auto', 'border-radius': '10px'},
                )
            )
        ], fluid=True),
    ], className="d-flex align-items-center justify-content-center",
        style={'height': '100vh', 'background-color': 'rgba(49, 97, 255, 0.52)'})

# dbc.Row(
#     dbc.Col([
#         dbc.InputGroup(
#             [
#                 dbc.InputGroupText(html.I(className="fas fa-envelope fa-lg", style={"color": "#6c757d"})),
#                 dbc.Input(type="email", placeholder="이메일", className="py-3", id='login-email'),
#             ],
#             className="mb-4 shadow-sm",
#         ),
#         dbc.InputGroup(
#             [
#                 dbc.InputGroupText(html.I(className="fas fa-lock fa-lg", style={"color": "#6c757d"})),
#                 dbc.Input(type="password", placeholder="비밀번호", className="py-3", id='login-password'),
#             ],
#             className="mb-4 shadow-sm",
#         ),
#         dbc.Button("로그인", color="primary", className="mb-3 d-block text-center align-items-center w-100",
#                    # href="/admin/main"),
#                    id="login-button"),
#         dbc.Button("회원가입", href="/admin/signup", className="button-link"),
#         dbc.Button("비밀번호 찾기", href='/admin/password', className="button-link"),
#         html.Div(id='login-message', className='mt-3')
#     ],
#         xs=12, sm=12, md=8, lg=6, xl=4, style={'margin': 'auto'},
#         className="p-4 shadow-sm rounded bg-white"
#     )
# )
