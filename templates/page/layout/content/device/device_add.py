from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


def device_add_layout():
    layout = html.Div([
        html.H1("장치 추가 페이지"),

    ])
    return layout
