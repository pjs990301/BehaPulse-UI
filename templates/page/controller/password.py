from app import admin_app
from flask import Flask
from dash import Dash, dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
import os


def password_controller(app):
    @app.callback(
        [Output('security-question', 'value'),
         Output('find-question-message', 'children')],
        [Input('find-password-email', 'n_blur')],
        [State('find-password-email', 'value')]
    )
    def update_security_question(n_blur, email):

        if n_blur is not None:
            if '@' not in email:
                return "", dbc.Alert("올바른 이메일 형식이 아닙니다.", color='danger')

            if (n_blur > 0) and email:
                api_url = f"{os.getenv('SERVER_IP')}/user/find_password/{email}"

                try:
                    response = requests.get(api_url)
                    if response.status_code == 200:
                        return response.json().get('securityQuestion'), ""
                    elif response.status_code == 404:
                        return "", dbc.Alert("계정을 찾을 수 없습니다.", color="danger")
                    else:
                        return "", dbc.Alert("서버 연결 실패", color="danger")

                except requests.exceptions.RequestException as e:
                    return "", dbc.Alert(f"An error occurred: {str(e)}", color="danger")

        return "", ""

    @app.callback(
        Output('find-password-message', 'children'),
        [Input('find-password-button', 'n_clicks')],
        [State('find-password-email', 'value'),
         State('security-question', 'value'),
         State('security-answer', 'value')]
    )
    def find_password(n_clicks, email, question, answer):
        if n_clicks is None:
            return ''

        if not email or not question or not answer:
            return dbc.Alert("모든 내용을 작성해주시기 바랍니다.", color="danger")

        api_url = f"{os.getenv('SERVER_IP')}/user/find_password/{email}"
        data = {
            "securityQuestion": question,
            "securityAnswer": answer
        }
        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 200:
                password = response.json().get('userPassword')
                return dbc.Alert(f"비밀번호 : {password}", color="success")
            elif response.status_code == 404:
                return dbc.Alert("계정을 찾을 수 없습니다.", color="warning")
            else:
                return dbc.Alert("비밀번호 찾기 실패", color="danger")

        except requests.exceptions.RequestException as e:
            return dbc.Alert(f"An error occurred: {str(e)}", color="danger")
