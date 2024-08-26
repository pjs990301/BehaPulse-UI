from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def login_layout():
    return html.Div([
        dbc.Container([
            dbc.Row(html.Img(src="assets/img/logo.svg", style={'width': '30vh'}),
                    className='align-items-center justify-content-center'),
            dbc.Row([
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(html.I(id='login-email-icon')),
                        dbc.Input(type="email", placeholder="이메일", className="", id='login-email'),
                    ], className="login-input-group w-100 mb-5", style={'height': '5vh'}),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText(html.I(id='login-password-icon')),
                        dbc.Input(type="password", placeholder="비밀번호", className="", id='login-password'),
                    ], className="login-input-group w-100 mb-5", style={'height': '5vh'}),

                dbc.Col([
                    dbc.Button("회원가입", href="/admin/signup", className="button-link w-20 h-20"),
                    dbc.Button("비밀번호 찾기", href='/admin/password', className="button-link w-20 h-20"),
                ], className='justify-content-between align-item-center',
                    style={'height': '5vh', 'align-content': 'center'}),

                dbc.Button("로그인", color="primary",
                           # href="/admin/main",
                           className="justify-content-center align-items-center",
                           style={'border-radius': '10px', 'background-color': 'rgba(49, 97, 255, 0.87)',
                                  'font-size': '1.5rem', 'height': '5vh', 'align-content': 'center'},
                           id="login-button"),
                html.Div(id='login-message', className='justify-content-center mt-3')

            ],
                className="shadow-lg bg-white justify-content-center p-4 m-2 d-flex align-items-center",
                style={'border-radius': '10px'}),
        ]),
    ], className="min-vh-100 d-flex",
        style={'background-color': 'rgba(49, 97, 255, 0.52)'}, )

