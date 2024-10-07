import webbrowser
from dash.dependencies import Input, Output, State, ALL
import urllib.parse

from flask import Flask, redirect, request, jsonify, session
import requests
import threading
import time
import hashlib
import base64
import os
import random
import urllib.parse as urlparse
from urllib.parse import urlencode, quote
from dash import Dash, dcc, html, callback_context, no_update
import logging
from dash.exceptions import PreventUpdate
from datetime import datetime
from dash import no_update, callback_context, State


import dash_bootstrap_components as dbc
import plotly.express as px


from ..layout.smartthings_device import create_smartthings_device_card



# from app import admin_app
def smartthings_device_controller(app):

    @app.callback(
        Output('cards-output', 'children'),
        [Input('login-button', 'n_clicks'), Input('url', 'pathname')]
    )
    # '''
    def update_token_output(n_clicks, pathname):
        # SmartThings API 토큰

        # API URL

        # 요청 헤더 설정

        # output = ''
        # access_token = request.cookies.get('access_token')
        # refresh_token = request.cookies.get('refresh_token')

        # session['mac_address_to_visualize'] = mac_addresses_to_visualize
        # session['mac_address_to_visualize'] = mac_addresses_to_visualize


        cards = []  # 여기에 생성된 카드들을 담을 리스트를 생성합니다.
        if 'access_token' in session and 'refresh_token' in session:
            # Get Access Token and Refresh Token From session
            access_token = session['access_token']
            refresh_token = session['refresh_token']
            url = 'https://api.smartthings.com/v1/devices'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            try:
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    devices = response.json()
                    for device in devices['items']:
                        cards.append(create_smartthings_device_card(
                            device['name'],
                            device['deviceId'],
                            device['name']))
                else:
                        # cards.append(create_device_card("No devices found", "Unknown MAC", "off"))
                    cards.append([])
            except requests.exceptions.RequestException as e:
                print(str(e))
                # cards.append(create_device_card("No devices found", "Unknown MAC", "off"))
                cards.append([])
        return cards  # 리스트로 반환

        
    @app.callback(
        Output('result', 'children'),
        Input({'type': 'smartthings-device-dots-icon', 'index': ALL, 'brightness': ALL}, 'n_clicks'),  # Input comes after Outputs,
        prevent_initial_call=True
    )
    def store_clicked_smartthings_deviceId(n_clicks):

        # Get Access Token and Refresh Token From session
        if 'access_token' in session and 'refresh_token' in session:
            access_token = session['access_token']
            refresh_token = session['refresh_token']

        print("clicked", callback_context)
        ctx = callback_context

        if not ctx.triggered or not n_clicks or all(click is None or click == 0 for click in n_clicks):
            raise PreventUpdate
        # 안전한 인덱스 참조를 위해 리스트 길이 확인
        clicked_id = None
        clicked_brightness_value = None
        for i, click in enumerate(n_clicks):
            if click and i < len(ctx.inputs_list[0]):  # 인덱스 범위 내에서 참조
                print('ctx.inputs_list[0][i]', ctx.inputs_list[0][i])
                clicked_id = ctx.inputs_list[0][i]['id']['index']
                clicked_brightness_value = ctx.inputs_list[0][i]['id']['brightness']
                break
        print("Clicked_id=", clicked_id, 'clicked_brightness_value=', clicked_brightness_value)
        if not clicked_id:
            raise PreventUpdate

        if clicked_id and clicked_brightness_value:
            # if access_token and refresh_token:
            if 'access_token' in session and 'refresh_token' in session:
                access_token = session['access_token']
                refresh_token = session['refresh_token']

                url = f'https://api.smartthings.com/v1/devices/{clicked_id}/commands'
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
                brightness = int(clicked_brightness_value)
                payload = {
                    "commands": [
                        {
                            "component": "main", 
                            "capability": "switchLevel",
                            "command": "setLevel",
                            "arguments": [brightness]  # Brightness Value (0-100)
                        }
                    ]
                }
                print("Trying to call API", url, payload, headers)
                response = requests.post(url, headers=headers, json=payload)
                print("Response:", response.status_code, response.text)
                if response.status_code == 200:
                    return f"전구의 밝기를 {brightness}%로 설정했습니다."
                else:
                    return f"오류 발생: {response.status_code}, {response.text}"
            else:
                return 'No Access token'
        else:
            raise PreventUpdate