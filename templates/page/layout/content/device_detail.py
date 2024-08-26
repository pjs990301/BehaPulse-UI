from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def create_detail_row(label, value, value_color="white"):
    status_color = "#00FF5D" if value == "on" else "#E50C0C"
    if label == "활성화 상태":
        value_color = status_color

    return dbc.Row([
        dbc.Col(
            html.Div(label, className="text-center", style={
                'font-size': '1rem',
                'background-color': 'None',
                'border': 'None',
                'color': 'white',
                'width': '100%',
                'height': '5vh',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center'

            }),
            width=3, className="d-flex justify-content-center mt-2 p-0"
        ),
        dbc.Col(
            html.Div(value, className="text-center", style={
                'font-size': '1rem',
                'background-color': '#8FA8FA',
                'border-radius': '20px',
                'color': value_color,
                'width': '100%',
                'height': '5vh',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center'
            }),
            width=8, className="d-flex justify-content-center mt-2 p-0 mx-2"
        )
    ], className="my-2 justify-content-center align-items-center")


def device_detail_layoout():
    return html.Div([
        dbc.Container([
            dbc.Row([
                html.Div([
                    html.I(id="fa-solid--laptop--device", style={'height': '8vh', 'width': '8vh'}),
                    html.I("Device", className="text-center", style={'font-size': '2rem', 'color': '#4C76FF'}),
                ], style={
                    'display': 'flex',
                    'align-items': 'center',  # Vertical alignment
                    'justify-content': 'center',  # Horizontal alignment
                    'height': '100%',  # Ensure it takes the full height of the parent container
                    'flex-direction': 'row'  # Align items in a row
                }),
            ], className="align-items-center justify-content-center mt-1"),

            dbc.Row([
                # create_detail_row("장치명", "ESP32"),
                # create_detail_row("Mac 주소", "00:00:00:00:00:00"),
                # create_detail_row("설치 장소", "길병원"),
                # create_detail_row("호실", "123호"),
                # create_detail_row("점검일", "24년 08월 08일"),
                # create_detail_row("활성화 상태", "on"),
                # create_detail_row("기타사항", "기기 변경 필요"),
                dcc.Loading(
                    id="loading-spinner",
                    type="default",  # 다른 스피너 유형을 원할 경우 변경 가능
                    children=[
                        dbc.Row(className='mt-3 p-0 align-items-center', id="device-detail-row",
                                style={'flex-wrap': 'wrap', 'justify-content': 'center'}),
                    ]
                    , style={'margin-top': '5vh'}
                ),

                dbc.Row(style={'flex-grow': '1'}),
                dbc.Col(
                    [
                        dbc.Button("수정", href="/admin/device/edit",
                                   className="detail_device_button align-items-center justify-content-center text-center d-flex",
                                   style={'font-size': '1rem', 'width': '30%'}),
                        dbc.Button("뒤로가기", href="/admin/device",
                                   className="detail_device_button align-items-center justify-content-center text-center d-flex",
                                   style={'font-size': '1rem', 'width': '30%', 'margin-left': '10px'}),
                    ], className="d-flex justify-content-end align-items-center"
                )

            ], className="mt-3 mx-1 p-2 justify-content-between",
                style={'background-color': 'rgba(143, 168, 250, 0.59)', 'height': '75vh', 'border-radius': '10px',
                       'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
                       }),
        ], className="p-2", fluid=True)
    ])
