from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


def edit_row(icon_class, label, value, placeholder):
    # 상태에 따른 색상 설정
    return html.Div(
        [
            # 왼쪽 아이콘
            html.Div([
                html.I(className=icon_class, style={'height': '5vh', 'width': '5vh'}),
            ], style={'display': 'flex', 'background-color': '#EEEEEE',
                      'justify-content': 'center', 'align-items': 'center',
                      'border-radius': '10px', 'width': '7vh', 'height': '7vh',
                      'margin-right': '20px'
                      },
            ),

            html.Div([
                dcc.Input(type='text',
                          placeholder=placeholder,
                          id=f'device-edit-input-{label}',
                          value=value,
                          className='device-edit-input'
                          )
            ], style={'display': 'inline-block', 'width': '80%', 'height': '7vh'},
            ),
        ], style={'display': 'flex', 'justify-content': 'start', 'align-items': 'center',
                  'padding': '10px 0px', 'width': '95%'},
    )


def edit_on_off(icon_class, on_style, off_style):
    return html.Div(
        [
            # 왼쪽 아이콘
            html.Div([
                html.I(className=icon_class, style={'height': '5vh', 'width': '5vh'}),
            ], style={'display': 'flex', 'background-color': '#EEEEEE',
                      'justify-content': 'center', 'align-items': 'center',
                      'border-radius': '10px', 'width': '7vh', 'height': '7vh',
                      'margin-right': '20px'
                      },
            ),
            html.Div([
                html.Div([
                    html.Span('ON', style=on_style,
                              id='on-button', n_clicks=0),
                    html.Span('OFF', style=off_style,
                              id='off-button', n_clicks=0),
                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),
            ], style={'display': 'flex', 'width': '80%', 'height': '7vh', 'align-items': 'center',
                      'padding': '0 10vh', 'font-size': '1rem'},
            ),
        ], style={'display': 'flex', 'justify-content': 'start', 'align-items': 'center',
                  'padding': '10px 0px', 'width': '95%'},
    )


def device_edit_layout():
    layout = html.Div([
        dcc.Location(id='device-edit', refresh=True),
        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='device-edit-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("장치 수정",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center mt-5 justify-content-center", )

            ],
                id='device-edit-header-content',
                className="d-flex justify-content-start mx-3",
            ),

            dcc.Loading(
                id="loading-spinner",
                type="circle",  # 다른 스피너 유형을 원할 경우 변경 가능
                children=html.Div([
                ], id='device-edit-main-content',
                    className="d-flex flex-column justify-content-center align-items-center my-3",
                    style={'height': '75vh'}),
            ),
            html.Div([
                dbc.Button([
                    # 아이콘과 텍스트를 버튼 안에 배치
                    html.I(className='ic-edit me-1', style={'width': '2rem', 'height': '2rem'}),
                    html.Span("수정하기", style={'font-size': '1rem', 'font-weight': 'bold'})
                ], color="primary", id='device-edit-save-button', href='/beha-pulse/main/device/edit/'),
            ], className='d-flex w-100 p-0', style={'justify-content': 'end'})
        ], className="d-flex flex-column w-100 flex-grow-1"),  # flex-grow-1을 사용해 상단과 중간 영역을 확장 가능하게 설정
    ], className="min-vh-100 d-flex flex-column bg-white")

    return layout
