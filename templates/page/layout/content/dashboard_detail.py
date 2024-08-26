from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go

fig = go.Figure(data=px.line(x=[1, 2, 3], y=[1, 3, 2]))
fig.update_layout(
    # margin=dict(l=10, r=10, t=10, b=10),
    margin=dict(l=0, r=10, t=0, b=0),
    xaxis_title='',
    yaxis_title='',
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    autosize=True,  # Automatically adjust size
)


def dashboard_detail_layout():
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
                dbc.Button("정보 보기",
                           href="/admin/dashboard/detail/info",
                           id='dashboard-info-button',
                           className="add_device align-items-center justify-content-center text-center d-flex",
                           style={'width': '15vh', 'font-size': '1.2rem'}),
                dbc.Button("뒤로가기", href="/admin/dashboard",
                           className="add_device align-items-center justify-content-center text-center d-flex",
                           style={'width': '15vh', 'font-size': '1.2rem', 'margin-left': '10px'}),
            ], className="justify-content-end mx-1"),

            dbc.Row([
                html.H1("홍길동",
                        id='dashboard-detail-name',
                        style={'font-size': '2rem', 'color': 'black', 'margin-top': '20px', 'text-align': 'center'}),
                html.H2("0000년 00월 00일 16:45:52",
                        id='dashboard-detail-date',
                        style={'font-size': '1.5rem', 'color': 'black', 'text-align': 'center'}),
                # dbc.Row([
                #     dcc.Graph(figure=fig, config={'displayModeBar': False}, style={'height': '100%', 'width': '100%'},
                #               className='p-0')
                # ],
                dbc.Row([
                    dcc.Graph(id='live-graph', animate=True,
                              config={'displayModeBar': False},
                              style={'height': '100%', 'width': '100%'},
                              className='p-0'),
                    dcc.Interval(
                        id='graph-update',
                        interval=200,  # Update graph every 200 milliseconds
                        n_intervals=0
                    ),
                ],
                    style={'height': '30vh', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
                    className="my-3 p-1"
                ),

                dbc.Row([
                    html.H4("현재 행동 상태 : 앉아 있음",
                            id = 'dashboard-detail-status',
                            style={'font-size': '1.5rem', 'color': 'black', 'text-align': 'center',
                                   'margin-top': '10px'}),
                    # html.H4("금일 낙상 횟수 : 25500000",
                    #         style={'font-size': '1.2rem', 'color': 'black', 'text-align': 'center',
                    #                'margin-top': '10px'}),
                    # html.H4("금일 누워 있던 누적 지속 시간 : 2500분 ",
                    #         style={'font-size': '1.2rem', 'color': 'black', 'text-align': 'center',
                    #                'margin-top': '10px'}),
                ], className="justify-content-center align-items-center mt-4 p-1"),

                html.Div(style={'flex-grow': '1'}),

            ], className="mt-3 mx-1 p-2 justify-content-between",
                style={'background-color': 'rgba(143, 168, 250, 0.59)', 'height': '70vh', 'border-radius': '10px',
                       'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
                       }),
        ], className="p-2", fluid=True)
    )
