# Flask Import
import json
from flask import Flask
from flask_restx import Api, Resource, reqparse, Namespace

# Namespace Import
from API import *

# Dash Import
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from templates.administrator.main import admin_app


app = Flask(__name__)

api = Api(app, version='1.0', title='API Document', description='Check the REST API specification.', doc='/doc/')
admin_app.init_app(app)
# dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')

# API에 네임스페이스 추가
api.add_namespace(user_ns)
api.add_namespace(room_ns)
api.add_namespace(user_room_ns)
api.add_namespace(device_ns)
api.add_namespace(user_device_ns)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
