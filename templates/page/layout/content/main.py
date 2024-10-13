from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


def main_content():
    print(session)
    content = html.Div([

        dbc.Row([
            html.Div([
                html.Img(src='../assets/img/sample_profile.png',
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
