from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


def user_content():
    content = html.Div([

        html.H1("유저 페이지"),
    ])
    return content
