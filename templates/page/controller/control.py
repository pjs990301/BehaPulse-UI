from dash.exceptions import PreventUpdate

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import requests
import json
from datetime import datetime

with open('config/server.json', 'r') as f:
    server = json.load(f)


def control_controller(app):
    @app.callback(
        Output('redirect', 'pathname', allow_duplicate=True),
        Input('control-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_main(n_clicks):
        if n_clicks:
            return '/beha-pulse/main/'

    @app.callback(
        Output('redirect', 'pathname', allow_duplicate=True),
        [Input('control-lying-down', 'n_clicks'),
         Input('control-falling-down', 'n_clicks'),
         Input('control-sitting-down', 'n_clicks')],
        prevent_initial_call=True
    )
    def control_data_store(lying_down, falling_down, sitting_down):
        if lying_down:
            session['status'] = 'lying_down'
            return '/beha-pulse/main/control/color/'
        elif falling_down:
            session['status'] = 'falling_down'
            return '/beha-pulse/main/control/color/'
        elif sitting_down:
            session['status'] = 'sitting_down'
            return '/beha-pulse/main/control/color/',
        else:
            return no_update

    @app.callback(
        Output('redirect', 'pathname', allow_duplicate=True),
        [Input('control-color-back-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def back_to_control(n_clicks):
        if n_clicks:
            return '/beha-pulse/main/control/'

    @app.callback(
        Output('test', 'children'),
        Input('url', 'pathname'),
    )
    def set_test(url):
        if url == '/beha-pulse/main/control/color/':
            return session['status']
        else:
            return no_update
