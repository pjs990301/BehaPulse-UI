# templates/administrator/main.py

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# layout
from .layout.login import login_layout

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

admin_app = dash.Dash(__name__, url_base_pathname='/admin/', external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
admin_app.layout = login_layout
