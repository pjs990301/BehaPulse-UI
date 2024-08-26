from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def create_device_card(device_name, mac_address, status):
    status_color = "#00FF5D" if status == "on" else "#E50C0C"

    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(device_name, width=3, style={'font-size': '1rem', 'color': 'white'},
                        className='text-center p-0'),
                dbc.Col(mac_address, width=6, style={'font-size': '1rem', 'color': 'white'},
                        className='text-center p-0'),
                dbc.Col([
                    status,
                    # dcc.Link(html.Img(src="assets/img/detail_device.svg", style={'margin-left': '20px'}),
                    #                  # href="/admin/device/detail"),
                    #                  href="/admin/device/detail",
                    #                  id={'type': 'device-dots-icon', 'index': mac_address}),
                    html.Img(src="assets/img/detail_device.svg", style={'margin-left': '20px', 'cursor': 'pointer'},
                             # href="/admin/device/detail",
                             id={'type': 'device-dots-icon', 'index': mac_address}
                             ),
                ], width=3, style={'font-size': '1rem', 'color': status_color}, className='text-center p-0')
            ]),
        ], style={'flex': '0 0'}),
        style={'background-color': '#8FA8FA', 'border-radius': '20px', 'margin-bottom': '10px', 'height': '5vh',
               'justify-content': 'center', 'border': 'None', 'width': '100%'}
    )


def device_layout():
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
                dbc.Button("장치 추가", href="/admin/device/add", id="add-device-button",
                           className="add_device align-items-center justify-content-center text-center d-flex",
                           style={'width': '15vh', 'font-size': '1.2rem'}),
            ], className="justify-content-end mx-1"),

            dbc.Row([
                dbc.Row([
                    dbc.Col('장치명', className='text-center p-0', style={'font-size': '1rem', 'color': 'white'}, width=3),
                    dbc.Col('MAC주소', className='text-center p-0', style={'font-size': '1rem', 'color': 'white'},
                            width=6),
                    dbc.Col('활성화상태', className='text-center p-0', style={'font-size': '1rem', 'color': 'white'},
                            width=3),
                ], className='mt-3 p-0 justify-content-center align-items-center', style={'height': '5vh'}),

                dcc.Loading(
                    id="loading-spinner",
                    type="default",  # 다른 스피너 유형을 원할 경우 변경 가능
                    children=dbc.Row(className='mt-3 p-0 align-items-center', id="device-cards-row",
                                     style={'width': '100%', 'flex-wrap': 'wrap', 'justify-content': 'center'}),
                ),

                dbc.Row(style={'flex-grow': '1', 'min-height': '50vh'}),

            ], className="mt-3 mx-1 p-2",
                style={'background-color': 'rgba(143, 168, 250, 0.59)', 'height': '70vh', 'border-radius': '10px',
                       'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'overflow-y': 'scroll',
                       'overflow-x': 'hidden', 'width': '100%', 'justify-content': 'center',
                       'scrollbar-width': 'none',  # Firefox에서 스크롤바 숨기기
                       '-ms-overflow-style': 'none',  # IE와 Edge에서 스크롤바 숨기기
                       }),
        ], className="p-2", fluid=True)
    ])
