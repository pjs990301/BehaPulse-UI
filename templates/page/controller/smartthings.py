from dash.dependencies import Input, Output
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
from dash import Dash, dcc, html, callback_context, no_update, State
from dash.exceptions import PreventUpdate
import logging

import requests
from requests.auth import HTTPBasicAuth

import dash
from dash.dependencies import Input, Output
from urllib.parse import parse_qs, urlparse

import os

base_oauth_url = 'https://api.smartthings.com/oauth'

verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
scopes = ['r:devices:*', 'w:devices:*', 'x:devices:*', 'r:hubs:*', 'r:locations:*', 'w:locations:*', 'x:locations:*', 'r:scenes:*', 'x:scenes:*', 'r:rules:*', 'w:rules:*']

login_failed = False
authentication_info = None
finish_url = os.getenv('SERVER_IP') + '/admin/smartthings' # Callback URL

# Define the necessary variables
client_id = os.getenv('CLIENT_ID') # OAuth Client Id
client_secret = os.getenv('CLIENT_SECRET') # OAuth Client Secret
redirect_uri = finish_url

def smartthings_controller(app):

    @app.callback(
        Output('token-output', 'children'),
        [Input('login-button', 'n_clicks'), Input('url', 'pathname')]
    )
    def update_token_output(n_clicks, pathname):
        authorize_url = f'{base_oauth_url}/authorize'
        params = {
            'scope': '+'.join(scopes),
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': finish_url,
        }
        authorize_url = f"{authorize_url}?{urlencode(params)}"
        authorize_url = authorize_url.replace('%2B', '+')

        if 'access_token' in session and 'refresh_token' in session:
            access_token = session['access_token']
            refresh_token = session['refresh_token']
            return html.A('삼성 계정 연동 완료. 클릭시 재연동 시도.', href=authorize_url)
        else:
            return html.A('클릭해서 삼성 계정을 연동하세요.', href=authorize_url)

    
    @app.callback(
        Output('access-token-output', 'children'),
        [Input('url', 'href')]  # URL of current page
    )
    def extract_access_token(href):
        if href is None:
            return "No URL provided."

        # Parse code from Query String - URL의 쿼리 스트링에서 파라미터 분석
        parsed_url = urlparse(href)
        query_params = parse_qs(parsed_url.query)

        # if 'code' parameter exists, parse that
        code_received = query_params.get('code', [None])[0]
        # access_token = session['access_token']
        if code_received:

            # Prepare the request URL and headers
            url = "https://api.smartthings.com/oauth/token"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            # Prepare the payload
            data = {
                'grant_type': 'authorization_code',
                'client_id': client_id,
                'code': code_received,
                'redirect_uri': redirect_uri
            }

            # Make the POST request
            response = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth(client_id, client_secret), timeout=10)

            # Check the response
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                refresh_token = token_data.get('refresh_token')
                print(f"Access Token: {access_token}")
                print(f"Refresh Token: {refresh_token}")
                if access_token:
                    session['access_token'] = access_token
                    session['refresh_token'] = refresh_token
                    return f"Access Token: {access_token}, and Refresh Token: {refresh_token}"
                else:
                    return "Access Token not found in URL."
            else:
                print(f"Failed to obtain access token: {response.status_code}, {response.text}")
                return f"Failed to obtain access token: {response.status_code}, {response.text}"
        else:
            return 'no code received'