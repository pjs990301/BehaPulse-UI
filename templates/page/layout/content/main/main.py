from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

def main_layout():
    layout = html.Div([
        dcc.Location(id='main', refresh=False),  # 페이지 이동을 위한 Location
        # 오버레이 배경
        html.Div(id='overlay-background', style={
            'display': 'none',
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'width': '100%',
            'height': '100%',
            'backgroundColor': 'rgba(0, 0, 0, 0.4)',
            'zIndex': 1
        }),

        # 오버레이 팝업 창
        html.Div(id='overlay-container', children=[
            html.Div([
                html.Div("길병원", style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer'}, id='gil-button'),
                html.Div("아산병원", style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer'}, id='asan-button'),
                html.Div("중앙병원", style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer'},
                         id='jungang-button')
            ], style={
                'background': '#fff',
                'border-radius': '30px',
                'drop-shadow': '0 4px 4px rgba(0, 0, 0, 0.25)',
                'width': '40vh',
                'margin': 'auto',
                'padding': '20px',
                'position': 'relative',
                'textAlign': 'center'
            })
        ], style={
            'display': 'none',
            'position': 'fixed',
            # 'top': '10vh',
            # 'left': '5vw',
            # 'transform': 'translate(-10vw, -10vh)',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'zIndex': 2
        }),

        # 상단 영역
        dbc.Container([
            # 상단 영역
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.Span("미사1동",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        style={'padding-right': '0.25rem'},
                        width="auto",
                    ),
                    dbc.Col(
                        html.I(className='ic-arrow-down', id='main-down-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        style={'padding-left': '0.25rem'},
                        width="auto",
                    ),

                ], className="align-items-center mt-5 mb-3 justify-content-center", )

            ],
                className="d-flex justify-content-start mx-3",
            ),
        ]),

        # 중앙 영역
        dbc.Container([
            html.Div(children=main_content(), id='main-content', className='d-flex h-100 w-100'),
        ], className='flex-grow-1'),

        # 하단 영역
        dbc.Container([
            html.Div(
                [
                    html.Div([
                        html.I(className='ic-home-selected', id='main-home-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("홈", className='text-bottom-selected'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-home-button'),
                    html.Div([
                        html.I(className='ic-desktop', id='main-device-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("장치", className='text-bottom'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-device-button'),
                    html.Div([
                        html.I(className='ic-incandescent', id='main-control-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("조명", className='text-bottom'),
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

def main_content():
    content = html.Div([

        dbc.Row([
            html.Div([
                html.Img(src='/assets/sample_profile.png',
                         # object-fit 추후 수정 필요
                         style={'width': '100%', 'height': '100%', 'objectFit': 'contain'}),
            ], className='main-profile-circle')
        ], className='d-flex justify-content-center align-items-center mb-4'),

        # Content Boxes
        dbc.Row(
            dbc.Card(
                dbc.CardBody("내가 관리하는 병원", style={'font-size': '1.2rem'}),
                className='main-card-body'
            ),
            className="main-card-container w-100 mx-3 my-2",
        ),

        # Content Boxes
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody("내 건강 상태", style={'font-size': '1.2rem'}),
                    className='main-card-body'
                ),
            ], style={'padding-right': '0.5rem', 'padding-left': '0rem'}),
            dbc.Col([
                dbc.Card(
                    dbc.CardBody("내 건강 상태", style={'font-size': '1.2rem'}),
                    className='main-card-body'
                ),
            ], style={'padding-left': '0.5rem', 'padding-right': '0rem'}),
        ], className="main-card-container w-100 mx-3 my-2", ),

        # Content Boxes
        dbc.Row(
            dbc.Card(
                dbc.CardBody("내 건강 상태", style={'font-size': '1.2rem'}),
                className='main-card-body'
            ),
            className="main-card-container w-100 mx-3 my-2",
        ),

    ], className="d-flex justify-content-center align-items-center flex-column w-100 h-100",
    )
    return content