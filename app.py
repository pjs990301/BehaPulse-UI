# Flask Import
import json
from datetime import timedelta

from flask import Flask, session
from flask_restx import Api, Resource, reqparse, Namespace
from flask_cors import CORS

# Namespace Import
from API import *

# Dash Import
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from templates.page.app import admin_app

# 데이터베이스 설정을 파일에서 불러옵니다.
with open('config/server.json', 'r') as f:
    server = json.load(f)


app = Flask(__name__)
CORS(app)  # To handle CORS issues between Flask and Dash

app.secret_key = "BehaPulse"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)  # 세션 유지 시간을 30분으로 설정

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
api.add_namespace(color_brightness_ns)

if __name__ == '__main__':
    app.run(host=server['server']['host'], port=server['server']['port'])
