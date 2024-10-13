from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


# 재사용 가능한 장치 항목 컴포넌트 함수
def info_row(icon_class, label, value):
    """장치 항목 컴포넌트"""
    return html.Div(
        [
            # 왼쪽 아이콘
            html.Div([
                html.I(className=icon_class, style={'height': '5vh', 'width': '5vh'}),
            ], style={'display': 'flex', 'background-color': '#EEEEEE',
                      'justify-content': 'center', 'align-items': 'center',
                      'border-radius': '10px', 'width': '7vh', 'height': '7vh'
                      },
                id='device-detail-icon'),
            # 중앙 라벨
            html.Div([
                html.Span(label, style={'font-size': '1rem'}),
            ], style={'display': 'inline-block'}, id='device-detail-label'),

            # 오른쪽 값
            html.Div([
                html.Span(value, style={'color': '#9C9C9C', 'font-size': '1rem'}),
            ], style={'display': 'inline-block'}, id='device-detail-value'),

        ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                  'padding': '10px 0px', 'width': '90%'},
    )


def device_detail_layout():
    layout = html.Div([
        dcc.Location(id='device-detail-url', refresh=True),
        html.Div(id='dummy-output', style={'display': 'none'}),  # Dummy Output 추가
        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='device-detail-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("장치 정보",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center my-5 justify-content-center", )

            ],
                id='device-detail-header-content',
                className="d-flex justify-content-start mx-3",
            ),

            html.Div([
                info_row('ic-manufacturing', 'ESP32', '장치'),
                info_row('ic-computer', '00:00:00:00:00:00', '장치'),
                info_row('ic-local-hospital', '길병원', '장치'),
                info_row('ic-location-on', '123호', '장치'),
                info_row('ic-calendar-month', '20240808', '장치'),
                info_row('ic-offline-bolt', 'ON', '장치'),
                info_row('ic-display-settings', '기기 변경 필요', '장치'),
                info_row('ic-person-device', '김철수', '장치'),
            ],
                className="d-flex flex-column justify-content-center align-items-center my-2",
                id='device-detail-main-content'
            ),
            html.Div([
                dbc.Button([
                    # 아이콘과 텍스트를 버튼 안에 배치
                    html.I(className='ic-edit me-1', style={'width': '2rem', 'height': '2rem'}),
                    html.Span("수정하기", style={'font-size': '1rem', 'font-weight': 'bold'})
                ], color="primary", id='device-edit-button'),
                dbc.Button([
                    # 아이콘과 텍스트를 버튼 안에 배치
                    html.I(className='ic-delete me-1', style={'width': '2rem', 'height': '2rem'}),
                    html.Span("삭제하기", style={'font-size': '1rem', 'font-weight': 'bold'})
                ], color="danger", id='device-delete-button')
            ], className='d-flex w-100 p-0', style={'justify-content': 'space-between'})
        ], className="d-flex flex-column w-100 flex-grow-1"),  # flex-grow-1을 사용해 상단과 중간 영역을 확장 가능하게 설정
    ], className="min-vh-100 d-flex flex-column bg-white")

    return layout
