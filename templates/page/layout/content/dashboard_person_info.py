from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def create_person_detail_row(label, value, input_type='text'):
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
            html.Div(value, className="text-center",
                     style={
                         'font-size': '1rem',
                         'background-color': '#8FA8FA',
                         'border-radius': '20px',
                         'color': 'white',
                         'width': '100%',
                         'height': '5vh',
                         'display': 'flex',
                         'align-items': 'center',
                         'justify-content': 'center'
                     }),
            width=8, className="d-flex justify-content-center mt-2 p-0 mx-2")
    ], className="my-2 justify-content-center align-items-center")


def dashboard_person_info_layout():
    return html.Div(
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

                # create_person_detail_row("성명", "김철수"),
                # create_person_detail_row("성별", "남"),
                # create_person_detail_row("생년월일", "0000년 00월 00일"),
                # create_person_detail_row("위치", "경기도 성남시 복정동"),

                dbc.Row(className='mt-3 p-0 align-items-center', id="person-detail-row",
                        style={'width': '100%', 'flex-wrap': 'wrap', 'justify-content': 'center'}),

                # Spacer div to push the button to the bottom
                html.Div(style={'flex-grow': '1'}),

                dbc.Col(
                    [
                        dbc.Button("수정", href="/admin/dashboard/detail/edit",
                                   className="detail_device_button align-items-center justify-content-center text-center d-flex",
                                   style={'font-size': '1rem', 'width': '30%'}),
                        dbc.Button("뒤로가기", href="/admin/dashboard/detail",
                                   className="detail_device_button align-items-center justify-content-center text-center d-flex",
                                   style={'font-size': '1rem', 'width': '30%', 'margin-left': '10px'}),
                    ], className="d-flex justify-content-end align-items-center"
                )
            ], className="mt-3 mx-1 p-2 justify-content-between",
                style={'background-color': 'rgba(143, 168, 250, 0.59)', 'height': '70vh', 'border-radius': '10px',
                       'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
                       }),
        ], className="p-2", fluid=True)
    )
