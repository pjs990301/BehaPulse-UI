from app import admin_app
from flask import Flask
from dash import Dash, dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
from dash import Dash, dcc, html, callback_context, no_update


def signup_controller(app):
    @app.callback(Output('signup-message', 'children'),
                  [Input('signup-button', 'n_clicks')],
                  [State('signup-name', 'value'),
                   State('signup-email', 'value'),
                   State('signup-password', 'value'),
                   State('signup-password-confirm', 'value'),
                   State('security-question', 'value'),
                   State('security-answer', 'value')])
    def signup(n_clicks, name, email, password, password_confirm, question, answer):
        if n_clicks is None:
            return ''

        if not name or not email or not password or not password_confirm or not question:
            return dbc.Alert("모든 내용을 작성해주시기 바랍니다.", color="danger")

        if password != password_confirm:
            return dbc.Alert("비밀번호와 비밀번호 확인란 불일치", color="danger")

        if '@' not in email:
            return dbc.Alert("올바른 이메일 형식이 아닙니다.", color='danger')

        api_url = "http://192.9.200.141:8000/admin/register"
        data = {
            "adminEmail": email,
            "adminName": name,
            "adminPassword": password,
            "securityQuestion": question,
            "securityAnswer": answer
        }
        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 201:
                return dbc.Alert("회원가입 성공!", color="success")
            elif response.status_code == 400:
                if response.json().get('message') == 'Admin already exists':
                    return dbc.Alert("이미 존재하는 계정입니다.", color="danger")
                else:
                    return dbc.Alert("회원가입 실패", color="danger")
            else:
                return dbc.Alert("서버 연결 실패", color="danger")

        except requests.exceptions.RequestException as e:
            return dbc.Alert(f"An error occurred: {str(e)}", color="danger")
