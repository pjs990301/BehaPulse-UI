from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from .sidebar import sidebar
from .topbar import topbar


def main_layout():
    print(session)
    layout = dbc.Container([
        dcc.Location(id='redirect', refresh=True),

        dbc.Button(
            id="navbar-toggler",
            color="None",
            style={"border": "None", 'width': '10vh', 'height': '10vh',
                   "background-image": "url('assets/img/navbar.svg')",
                   "background-size": "cover",
                   "background-repeat": "no-repeat",
                   "background-position": "center center",
                   }
        ),

        html.Div(id='dummy-div', style={'display': 'none'}),

        # Overlay for detecting outside clicks
        html.Div(id='overlay', style={
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
            "background-color": "rgba(0,0,0,0.5)",
            "display": "none",  # Initially hidden
            "z-index": "9998",  # Just below the sidebar
        }),

        # Sidebar
        html.Div([
            sidebar()
        ], id="sidebar", style={
            "position": "absolute",
            # "top": "-120%",  # Initially hide the sidebar off-screen above
            "top": "50px",  # Initially hide the sidebar off-screen above
            "left": "0px",  # Initial left position
            "height": "80vh",
            "width": "10vh",
            "background-image": "url('assets/img/full_navbar.svg')",
            "background-size": "cover",
            "background-repeat": "no-repeat",
            "background-position": "center",

            "transform": "translateY(-120%)",  # Initially hide the sidebar off-screen above
            "transition": "transform 0.3s ease",
            "z-index": "9999",
            "overflow": "hidden"
        }),


        html.Div(id="page-content"),

    ], className="min-vh-100")
    return layout
