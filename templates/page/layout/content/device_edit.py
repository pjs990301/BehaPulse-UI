from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def create_detail_edit_row(label, value, input_type='text', value_color="white"):
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
            dbc.Input(value=value, placeholder=value, className="text-center", type=input_type,
                      id=f"device-edit-{label}",
                      style={
                          'font-size': '1rem',
                          'background-color': '#8FA8FA',
                          'border-radius': '20px',
                          'border': 'None',
                          'color': value_color,
                          'width': '100%',
                          'height': '5vh',
                          'display': 'flex',
                          'align-items': 'center',
                          'justify-content': 'center'
                      }),
            width=8, className="d-flex justify-content-center mt-2 p-0 mx-2")
    ], className="my-2 justify-content-center align-items-center")


def create_detail_on_off(label, on_style, off_style):
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
        dbc.Col([
            html.Div([
                html.Span("on", id="on-button", n_clicks=0, style=on_style),
                html.Span("off", id="off-button", n_clicks=0, style=off_style),
            ], id="toggle-container", style={
                'background-color': '#8FA8FA',
                'border-radius': '20px',
                'width': '100%',
                'height': '5vh',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center'
            }),
        ], width=8, className="d-flex justify-content-center mt-2 p-0 mx-2"),
    ], className="my-2 justify-content-center align-items-center")


def create_edit_person_row(label, value):
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
            dcc.Dropdown(
                className="text-center device-dropdown",
                id='device-edit-person-dropdown',
                placeholder="사용자선택",
                # style={
                #     'font-size': '1rem',
                #     'background-color': '#8FA8FA',
                #     'border-radius': '20px',
                #     'border': 'None',
                #     'color': 'white',
                #     'width': '100%',
                #     'height': '5vh',
                #     'display': 'flex',
                #     'align-items': 'center',
                #     'justify-content': 'center'
                # },
                options=[
                    # {'label': label, 'value': value}
                ]
            ),
            width=8, className="justify-content-center mt-2 p-0 mx-2")
    ], className="my-2 justify-content-center align-items-center")


def device_edit_layout():
    return html.Div([
        html.Div(id='hidden-div-device-edit', style={'display': 'none'}),
        html.Div(id='hidden-div-device-delete', style={'display': 'none'}),

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
                # create_detail_edit_row("장치명", "ESP32"),
                # create_detail_edit_row("Mac 주소", "00:00:00:00:00:00"),
                # create_detail_edit_row("설치 장소", "길병원"),
                # create_detail_edit_row("호실", "123호"),
                # create_detail_edit_row("점검일", "24년 08월 08일"),
                # create_detail_edit_row("활성화 상태"),
                # create_detail_edit_row("기타사항", "기기 변경 필요"),

                dcc.Loading(
                    id="loading-spinner",
                    type="default",  # 다른 스피너 유형을 원할 경우 변경 가능
                    children=[
                        dbc.Row(className='mt-3 p-0 align-items-center', id="device-detail-edit-row",
                                style={'flex-wrap': 'wrap', 'justify-content': 'center'}),
                        create_edit_person_row("사용자", ""),
                    ]
                ),
                dbc.Row(style={'flex-grow': '1'}),
                dbc.Col(
                    [
                        dbc.Button("저장",
                                   id='device-edit-save-button', n_clicks=0,
                                   href="/admin/device",
                                   className="detail_device_button align-items-center justify-content-center text-center d-flex",
                                   style={'font-size': '1rem', 'width': '30%'}),
                        dbc.Button("삭제",
                                   id='device-edit-delete-button', n_clicks=0,
                                   href="/admin/device",
                                   className="detail_device_button align-items-center justify-content-center text-center d-flex",
                                   style={'font-size': '1rem', 'width': '30%', 'margin-left': '10px'}),
                        dbc.Button("취소", href="/admin/device",
                                   className="detail_device_button align-items-center justify-content-center text-center d-flex",
                                   style={'font-size': '1rem', 'width': '30%', 'margin-left': '10px'}),
                    ], className="d-flex justify-content-end align-items-center mt-1"
                )
            ], className="mt-3 mx-1 p-2 justify-content-between",
                style={'background-color': 'rgba(143, 168, 250, 0.59)', 'height': '75vh', 'border-radius': '10px',
                       'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
                       }),
        ], className="p-2", fluid=True)
    ])
