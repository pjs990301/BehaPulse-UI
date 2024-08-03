from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

login_user_email = dbc.Input(type="email", id="login-email", placeholder="Enter email")

login_user_password = dbc.Input(type="password", id="login-password", placeholder="Password"),


