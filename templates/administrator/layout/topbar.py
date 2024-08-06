from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def topbar():
    return html.Div(
        [
            dbc.Row(
                # 검색창
                dcc.Input(id='search-input', type='text', placeholder='Search...', className='form-control',
                          style={'width': '50%', 'margin-left': '4rem'}),
                # 프로필 이미지

                # 드롭다운

            ),

        ], className="m-3"
    )
