from app import admin_app
from flask import Flask
from dash import Dash, dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests


def login_controller(app):
    @app.callback(Output('login-message', 'children'),
                        [Input('login-button', 'n_clicks')],
                        [State('login-email', 'value'),
                         State('login-password', 'value')])
    def login(n_clicks, email, password):
        if n_clicks is None:
            return ''

        if not email or not password:
            return dbc.Alert("이메일과 비밀번호를 모두 입력해주세요.", color="danger")

        api_url = "http://192.9.200.141:8000/admin/login"
        data = {
            "adminEmail": email,
            "adminPassword": password
        }

        try:
            response = requests.post(api_url, json=data)

            # Handle the response
            if response.status_code == 200:
                return dbc.Alert("로그인 성공!", color="success")
            elif response.status_code == 404:
                return dbc.Alert('이메일 혹은 비밀번호가 잘못 입력되었습니다.', color="danger")
            else:
                return dbc.Alert("서버 연결 실패", color="danger")

        except requests.exceptions.RequestException as e:
            return dbc.Alert(f"An error occurred: {str(e)}", color="danger")
