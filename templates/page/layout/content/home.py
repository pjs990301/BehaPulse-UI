from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def home_layout():
    return html.Div(
        dbc.Container([
            dbc.Row(html.Img(src="assets/img/main_logo.svg", style={'height': '15vh'}),
                    className='align-items-center justify-content-center mt-3'
                    ),
            dbc.Row(html.Img(src="assets/img/main_monitor.svg", style={'height': '35vh'})),
            dbc.Row([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.I(id='pepicons-pop--monitor-loop', style={'height': '8vh', 'width': '8vh'}),
                            html.P(["비접촉식", html.Br(), "모니터링"], className="text-center",
                                   style={'font-size': '1.2rem'})
                        ], style={'text-align': 'center', 'display': 'flex', 'flex-direction': 'column',
                                  'align-items': 'center'})
                    ], className="p-0 mx-1"),
                    dbc.Col([
                        html.Div([
                            html.I(id='game-icons--feather', style={'height': '8vh', 'width': '8vh'}),
                            html.P("경량화된 설계", className="text-center", style={'font-size': '1.2rem'})
                        ], style={'text-align': 'center', 'display': 'flex', 'flex-direction': 'column',
                                  'align-items': 'center'})
                    ], className="p-0 mx-1"),
                    dbc.Col([
                        html.Div([
                            html.I(id='fluent--location-live-20-regular', style={'height': '8vh', 'width': '8vh'}),
                            html.P("실시간 데이터 전송 및 분석", className="text-center", style={'font-size': '1.2rem'})
                        ], style={'text-align': 'center', 'display': 'flex', 'flex-direction': 'column',
                                  'align-items': 'center'})
                    ], className="p-0 mx-1"),
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.I(id='tdesign--wry-smile', style={'height': '8vh', 'width': '8vh'}),
                            html.P("사용자 친화적 인터페이스", className="text-center", style={'font-size': '1.2rem'})
                        ], style={'text-align': 'center', 'display': 'flex', 'flex-direction': 'column',
                                  'align-items': 'center'})
                    ], className="p-0 mx-1"),
                    dbc.Col([
                        html.Div([
                            html.I(id='eos-icons--iot', style={'height': '8vh', 'width': '8vh', 'display': 'block'}),
                            html.P("IoT API 활용", className="text-center", style={'font-size': '1.2rem'})
                        ], style={'text-align': 'center', 'display': 'flex', 'flex-direction': 'column',
                                  'align-items': 'center'})
                    ], className="p-0 mx-1"),
                    dbc.Col([
                        html.Div([
                            html.I(id='eos-icons--ai', style={'height': '8vh', 'width': '8vh', 'display': 'block'}),
                            html.P("On-Device AI", className="text-center", style={'font-size': '1.2rem'})
                        ], style={'text-align': 'center', 'display': 'flex', 'flex-direction': 'column',
                                  'align-items': 'center'})
                    ], className="p-0 mx-1"),
                ])
            ], className='justify-content-center align-items-center p-0.5', style={'color': '#699bf7'}),

        ])
    )
