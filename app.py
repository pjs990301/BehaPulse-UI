# Flask Import
import json
from datetime import timedelta, datetime
import requests
from flask import Flask, session, request, jsonify
from flask_restx import Api, Resource, reqparse, Namespace
from flask_cors import CORS

# Namespace Import
from API import *

# Dash Import
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from templates.page.app import admin_app

import ssl
import os

app = Flask(__name__)
CORS(app)  # To handle CORS issues between Flask and Dash

app.secret_key = "BehaPulse"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # 세션 유지 시간을 30분으로 설정

api = Api(app, version='1.0', title='API Document', description='Check the REST API specification.', doc='/doc/')
admin_app.init_app(app)
# dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')

# API에 네임스페이스 추가
api.add_namespace(user_ns)
api.add_namespace(device_ns)
api.add_namespace(user_device_ns)
api.add_namespace(dashboard_ns)
api.add_namespace(user_dashboard_ns)
api.add_namespace(user_dashboard_device_ns)

@app.route('/smartthings/', methods=['GET'])
def get_local_time():
    # 현재 로컬 시간
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 요청 헤더 가져오기
    headers = request.headers

    # 요청 바디 가져오기 (GET 요청에서는 body가 없을 수 있음)
    body = request.get_data(as_text=True)

    # 헤더와 바디를 <pre> 태그로 감싸기
    headers_formatted = f'<pre>{headers}</pre>'
    print(headers_formatted)
    body_formatted = f'<pre>{body}</pre>'

    # 시간과 함께 반환
    return f'<h1>{current_time}</h1>{headers_formatted}{body_formatted}'


# SmartThings 인증 관련(Valid Domain-SmartApp)
@app.route('/admin/smartthings/', methods=['POST'])
def get_request_details():
    body = request.get_json()
    print("Body", body)

    if body.get('lifecycle') == 'CONFIRMATION':
        confirmation_url = body['confirmationData']['confirmationUrl']
        
        try:
            # SmartThings에 GET 요청 보내기
            response = requests.get(confirmation_url)
            response.raise_for_status()  # 요청이 성공했는지 확인
            print(response.raise_for_status())
            return jsonify({'message': 'CONFIRMATION success'}), 200
        except requests.exceptions.RequestException as e:
            print(f'Error confirming SmartThings registration: {e}')
            return jsonify({'message': 'CONFIRMATION failed'}), 500
    else:
        return jsonify({'message': 'Not a confirmation request'}), 200

def load_env_file(file_path):
    # 파일을 열고 한 줄씩 읽음
    with open(file_path, 'r') as file:
        for line in file:
            # 주석이거나 빈 줄이면 건너뜀
            if line.startswith('#') or not line.strip():
                continue
            
            # 'KEY=VALUE' 형식의 줄을 파싱
            key, value = line.strip().split('=', 1)
            # 환경 변수로 설정
            os.environ[key] = value

load_env_file('.env')

if __name__ == '__main__':
    context = ('/path/to/letsencrypt/live/smart.musicnjoy.art/fullchain.pem', '/path/to/letsencrypt/live/smart.musicnjoy.art/privkey.pem')
    app.run(host='0.0.0.0', port=443, ssl_context=context)
