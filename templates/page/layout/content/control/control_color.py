from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
import dash_daq as daq


def control_color_layout():
    layout = html.Div([
        dcc.Store(id='control-data-store', data={}),

        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='control-color-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("조명 관리",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center mt-5 mb-5 justify-content-center", )

            ],
                className="d-flex justify-content-start mx-3",
            ),
        ]),

        dbc.Container([
            html.Div(children=control_content(), id='main-content', className='d-flex w-100', )
        ], className='flex-grow-1'),

        # 하단 영역
        dbc.Container([
            html.Div(
                [
                    html.Div([
                        html.I(className='ic-home', id='main-home-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("홈", className='text-bottom'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-home-button'),
                    html.Div([
                        html.I(className='ic-desktop', id='main-device-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("장치", className='text-bottom'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-device-button'),
                    html.Div([
                        html.I(className='ic-incandescent-selected', id='main-control-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("조명", className='text-bottom-selected'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-control-button'),
                    html.Div([
                        html.I(className='ic-health-metrics', id='main-dashboard-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("대시보드", className='text-bottom'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-dashboard-button'),
                    html.Div([
                        html.I(className='ic-more', id='main-more-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("더보기", className='text-bottom'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-more-button'),
                ],
                className='d-flex justify-content-around align-items-center w-100',
            ),
        ],
            className='w-100 d-flex justify-content-end align-items-center mb-1',
            style={'height': '10vh', 'border-top': '1px solid rgba(0, 0, 0, 0.1)'}),
    ], className="min-vh-100 d-flex flex-column bg-white")

    return layout


def control_content():
    content = html.Div([
        # Brightness Slider
        html.Div([
            dcc.Slider(
                id='brightness-slider',
                min=0,
                max=100,
                value=50,
                marks={0: '0%', 100: '100%'},
                step=1
            ),
            html.Div([
                html.Span('🌞', style={'font-size': '20px', 'margin-right': '10px'}),
                html.Span('🌞', style={'font-size': '20px', 'margin-left': '10px'}),
            ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'margin-top': '-10px'}),
        ], style={'margin-bottom': '20px'}),

        # Color Wheel using iro.js
        html.Div([
            html.Div(id="colorWheel", style={'height': '250px', 'width': '250px', 'margin': '0 auto'}),
            html.Div(id='selected-color', style={'textAlign': 'center', 'marginTop': '20px', 'fontSize': '20px'}),
        ], style={'textAlign': 'center'}),

        # Save Button
        html.Div([
            dbc.Button('저장하기', id='save-button', color='primary', size='lg', style={'width': '100%'})
        ], style={'text-align': 'center', 'margin-top': '30px', 'padding': '0 20px'}),

        # Load the iro.js library from the correct CDN version (stable)
        html.Script(src="https://cdn.jsdelivr.net/npm/@jaames/iro@5.5.0/dist/iro.min.js"),

        # JavaScript to initialize the color picker
        html.Script('''
        document.addEventListener('DOMContentLoaded', function() {
            var colorPicker = new iro.ColorPicker("#colorWheel", {
                width: 250,
                color: "#18E8FF",
                borderWidth: 1,
                borderColor: "#00A9E0",
            });
            colorPicker.on('color:change', function(color) {
                // Send color to Dash
                const hexColor = color.hexString;
                document.getElementById('selected-color').innerHTML = 'Selected Color: ' + hexColor;
            });
        });
    ''')
    ])
    return content
