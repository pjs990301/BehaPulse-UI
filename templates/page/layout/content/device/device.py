from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

# 색상 정의
status_colors = {
    "active": "#00D84F",  # 녹색
    "inactive": "#E10000"  # 빨간색
}


# 재사용 가능한 장치 항목 컴포넌트 함수
def device_item(name, mac_address, status):
    """장치 항목 컴포넌트"""
    return html.Div(
        [
            # 왼쪽 장치 정보
            html.Div([
                html.Div(name, style={'font-weight': 'bold', 'font-size': '20px'}),
                html.Div(mac_address, style={'color': 'grey', 'font-size': '14px'}),
            ], style={'display': 'inline-block'}),

            # 오른쪽 상태 아이콘
            html.Div([
                html.Span(style={
                    'backgroundColor': status_colors[status],
                    'width': '2.5vh',
                    'height': '2.5vh',
                    'border-radius': '6px',
                    'display': 'inline-block'
                })
            ], style={'display': 'inline-block'}),

        ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                  'padding': '10px 0px', 'border-bottom': '1px solid #C5C5C5',
                  'width': '100%'},

        # 행 전체가 클릭되도록 설정 (n_clicks 속성 추가)
        id={'type': 'device-row', 'index': mac_address},  # 각 줄에 고유 id 부여
        n_clicks=0,  # 클릭 수 초기화
    )


def device_content():
    content = html.Div([
        dcc.Store(id='device-data-store', data={}),  # 데이터를 저장할 숨겨진 Store
        html.Div(id='dummy-output', style={'display': 'none'}),  # Dummy Output 추가
        dcc.Location(id='device', refresh=True),  # 페이지 이동을 위한 Location
        dbc.Row([
            # 제목
            html.Span("장치 정보", style={'font-size': '1.25rem', 'font-weight': 'bold', 'padding': '0px'}),

            dcc.Loading(
                id="loading-spinner",
                type="circle",  # 다른 스피너 유형을 원할 경우 변경 가능
                children=html.Div(id='device-rows', className='w-100 mb-3',
                                  style={'height': '65vh', 'overflow-y': 'auto'},),
            ),

            html.Div([
                dbc.Button([
                    # 아이콘과 텍스트를 버튼 안에 배치
                    html.I(className='ic-device-add me-1', style={'width': '2rem', 'height': '2rem'}),
                    html.Span("장치 추가", style={'font-size': '1rem', 'font-weight': 'bold'})
                ], color="primary", id='device-add-button')
            ], className='d-flex justify-content-end w-100 p-0')
        ], className='w-100'),

    ], className="d-flex align-items-center flex-column mx-3 h-100 w-100 justify-content-center")

    return content
