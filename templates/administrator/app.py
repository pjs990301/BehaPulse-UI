import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# layout
from .layout import set_layout, set_content

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
icon_css = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css"
admin_app = dash.Dash(__name__, url_base_pathname='/admin/',
                      external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css, icon_css],
                      suppress_callback_exceptions=True)

admin_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page', style={'height': '100vh'}),
])

admin_app.title = "Admin Page"

set_layout(admin_app)
set_content(admin_app)