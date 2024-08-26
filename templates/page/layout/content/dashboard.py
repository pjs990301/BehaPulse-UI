from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def create_dashboard_card(person_id, name, gender, birth, status):
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(name, width=2, style={'font-size': '1rem', 'color': 'white'}, className='text-center p-0'),
                dbc.Col(gender, width=2, style={'font-size': '1rem', 'color': 'white'}, className='text-center p-0'),
                dbc.Col(birth, width=4, style={'font-size': '1rem', 'color': 'white'}, className='text-center p-0'),
                dbc.Col(
                    [status,
                     html.Img(src="assets/img/detail_device.svg", style={'margin-left': '20px', 'cursor': 'pointer'},
                              id={'type': 'dashboard-dots-icon', 'index': person_id}
                              )

                     ], width=4, style={'font-size': '1rem', 'color': 'white'}, className='text-center p-0')
            ]),
        ], style={'flex': '0 0', 'padding': '0.5rem'}),
        style={'background-color': '#8FA8FA', 'border-radius': '20px', 'margin-bottom': '10px', 'height': '5vh',
               'justify-content': 'center', 'border': 'None', 'width': '100%'}
    )


def dashbord_layout():
    return html.Div([
        dcc.Location(id='dashboard-url', refresh=False),
        dbc.Container([
            dbc.Row([
                html.Div([
                    html.I(id="prime--chart-line--dashboard", style={'height': '8vh', 'width': '8vh'}),
                    html.I("Dashboard", className="text-center", style={'font-size': '2rem', 'color': '#4C76FF'}),
                ], style={
                    'display': 'flex',
                    'align-items': 'center',  # Vertical alignment
                    'justify-content': 'center',  # Horizontal alignment
                    'height': '100%',  # Ensure it takes the full height of the parent container
                    'flex-direction': 'row'  # Align items in a row
                }),
            ], className="align-items-center justify-content-center mt-1"),

            dbc.Row([
                dbc.Button("인원 추가", href="/admin/dashboard/add", id="add-dashbaord-button",
                           className="add_device align-items-center justify-content-center text-center d-flex",
                           style={'width': '15vh', 'font-size': '1.2rem'}),
            ], className="justify-content-end mx-1"),

            dbc.Row([
                dbc.Row([
                    dbc.Col('성명', className='text-center p-0', style={'font-size': '1rem', 'color': 'white'}, width=2),
                    dbc.Col('성별', className='text-center p-0', style={'font-size': '1rem', 'color': 'white'}, width=2),
                    dbc.Col('생년월일', className='text-center p-0', style={'font-size': '1rem', 'color': 'white'},
                            width=4),
                    dbc.Col('행동상태', className='text-center p-0', style={'font-size': '1rem', 'color': 'white'},
                            width=4),
                ], className='mt-3 p-0 justify-content-center align-items-center', style={'height': '5vh'}),

                dcc.Loading(
                    id="loading-spinner",
                    type="default",  # 다른 스피너 유형을 원할 경우 변경 가능
                    children=dbc.Row(className='mt-3 p-0 align-items-center', id="dashboard-cards-row",
                                     style={'flex-wrap': 'wrap', 'justify-content': 'center'}),
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
