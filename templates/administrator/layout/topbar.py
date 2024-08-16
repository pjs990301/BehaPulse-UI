from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


# def topbar():
#     return html.Div(
#         [
#             dbc.Row(
#                 [
#                     dbc.Col([dbc.Col(html.H3("Hello Kruluz Utsman", className=""), width="auto"),
#                              dbc.Col(html.Small("4:45 pm 19 Jan 2022", className="mb-2"), width="auto"),
#                              ]),
#
#                     dbc.Col(html.I(className="fas fa-users"), width="auto")
#                 ],
#                 justify="between",
#                 align="center",
#             ),
#
#         ], className="m-4"
#     )

def topbar():
    return html.Div(
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    dbc.DropdownMenu(
                        label="즐겨찾기에 추가된 장소",
                        id="topbar-dropdown",
                        children=[
                            dbc.DropdownMenuItem("1", href="#"),
                            dbc.DropdownMenuItem("2", href="#"),
                            dbc.DropdownMenuItem("3", href="#"),
                        ],
                        direction="down",
                    ),
                    width=1),

                dbc.Col(width=9),

                dbc.Col(
                    dbc.Nav([
                        dbc.NavLink(html.I(className="fas fa-plus fa-lg m-3"), href='#'),
                        dbc.NavLink(html.I(className="fas fa-bell fa-lg m-3"), href='#'),
                        dbc.NavLink(html.I(className="fas fa-magnifying-glass fa-lg m-3"), href='#'),
                    ]), width=2, className="d-flex justify-content-center align-items-center")
            ]),
        ], fluid=True),
        className="m-4"
    )
