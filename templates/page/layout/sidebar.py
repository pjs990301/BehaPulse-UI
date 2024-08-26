from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


# Define the sidebar layout
def sidebar():
    return html.Div(
        [
            html.P("홍길동님", className="text-center mt-2 text-white px-0", style={'font-size': '1.2rem'},
                   id="sidebar-userName"),
            dbc.Nav(
                [
                    dbc.NavLink(
                        [html.I(id="solar--home-bold", style={'height': '5vh', 'width': '5vh'}),
                         html.P("Home", className="m-0")],
                        # active="exact",
                        href="/admin/home", className="custom-navlink my-4"),
                    dbc.NavLink(
                        [html.I(id="fa-solid--laptop", style={'height': '5vh', 'width': '5vh'}),
                         html.P("Device", className="m-0")],
                        # active="exact",
                        href="/admin/device", className="custom-navlink my-4"),
                    dbc.NavLink(
                        [html.I(id="prime--chart-line", style={'height': '5vh', 'width': '5vh'}),
                         html.P("Dashboard", className="m-0")],
                        # active="exact",
                        href="/admin/dashboard", className="custom-navlink my-4"),
                ],
                vertical=True,
                pills=True,
                className="my-3"
            ),
            html.Div(
                [
                    dbc.Button("로그아웃", id="logout-button", color="None"),
                    html.P(["0000년 00월 00일", html.Br(), "00시 00분"], className="text-center mt-2", id="date-time",
                           style={"font-size": "0.5rem", 'color': 'white'})
                ]
                , className="text-center mt-2", id="sidebar-footer",
                style={
                    'postion': 'absolute',
                    'bottom': '0px',
                    'justify-content': 'center',
                    'align-items': 'center',
                }
            ),
            # 시간 업데이트를 위한 인터벌 설정
            dcc.Interval(
                id='interval-component',
                interval=60 * 1000,  # 1분 간격 (밀리초 단위)
                n_intervals=0
            )
        ], id="sidebar-content",
        style={
            "top": "0px",
            'position': 'absolute',
            "width": "10vh",
            'align-items': 'center',
            'display': 'flex',
            'flex-direction': 'column',
            'justify-content': 'space-between',
        }
    )
