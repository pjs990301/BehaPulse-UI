from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


def dashboard_content():
    content = html.Div([

        html.H1("대시보드 페이지"),
    ])
    return content
