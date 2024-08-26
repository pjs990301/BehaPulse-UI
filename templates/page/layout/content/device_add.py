from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def create_detail_row_add(label, value, input_type='text', value_color="white"):
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
            dbc.Input(placeholder=value, className="text-center", type=input_type,
                      id=f"device-add-{label}",
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


def create_add_person_row(label, value):
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
                id='device-add-person-dropdown',
                placeholder="사용자선택",
                # style={
                # },
                options=[
                    # {'label': label, 'value': value}
                ]
            ),
            width=8, className="justify-content-center mt-2 p-0 mx-2")
    ], className="my-2 justify-content-center align-items-center")


def device_add_layout():
    return html.Div(
        [
            html.Div(id='hidden-div-device-add', style={'display': 'none'}),

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
                    dcc.Loading(
                        id="loading-spinner",
                        type="default",  # 다른 스피너 유형을 원할 경우 변경 가능
                        children=[
                            dbc.Row(
                                [
                                    create_detail_row_add("장치명", ""),
                                    create_detail_row_add("Mac 주소", ""),
                                    create_detail_row_add("설치 장소", ""),
                                    create_detail_row_add("호실", ""),
                                    create_detail_row_add("점검일", ""),
                                    create_detail_on_off("활성화 상태",
                                                         on_style={
                                                             'cursor': 'pointer',
                                                             'color': 'white',
                                                             'font-size': '1rem',
                                                             'padding': '0px 20px'
                                                         },
                                                         off_style={
                                                             'cursor': 'pointer',
                                                             'color': 'white',
                                                             'font-size': '1rem',
                                                             'padding': '0px 20px'
                                                         }),
                                    create_detail_row_add("기타사항", ""),
                                    create_add_person_row("사용자", ""),
                                ],
                                className='mt-3 p-0 align-items-center', id="device-add-row",
                                style={'flex-wrap': 'wrap', 'justify-content': 'center'}
                            ),
                        ]
                    ),

                    # Spacer div to push the button to the bottom
                    dbc.Row(style={'flex-grow': '1'}),

                    dbc.Col(
                        [
                            dbc.Button("추가",
                                       href="/admin/device",
                                       id='device-add-save-button', n_clicks=0,
                                       className="detail_device_button align-items-center justify-content-center text-center d-flex",
                                       style={'font-size': '1rem', 'width': '30%'}),
                            dbc.Button("뒤로가기", href="/admin/device",
                                       className="detail_device_button align-items-center justify-content-center text-center d-flex",
                                       style={'font-size': '1rem', 'width': '30%', 'margin-left': '10px'}),
                        ], className="d-flex justify-content-end align-items-center"
                    )
                ], className="mt-3 mx-1 p-2 justify-content-between",
                    style={'background-color': 'rgba(143, 168, 250, 0.59)', 'height': '75vh',
                           'border-radius': '10px',
                           'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
                           }),
            ], className="p-2", fluid=True)
        ])
