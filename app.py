# Flask Import
import json
from flask import Flask
from flask_restx import Api, Resource, reqparse, Namespace

# Namespace Import
from API import *

# Dash Import
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = Flask(__name__)

api = Api(app, version='1.0', title='API Document', description='Check the REST API specification.')
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')

# Dash 레이아웃 정의
dash_app.layout = html.Div(children=[
    html.H1('My Dash App with Flask'),
])

# API에 네임스페이스 추가
api.add_namespace(user_ns)
api.add_namespace(room_ns)
api.add_namespace(user_room_ns)
api.add_namespace(device_ns)
api.add_namespace(user_device_ns)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
