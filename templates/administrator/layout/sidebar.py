from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


# Define the sidebar layout
def sidebar():
    return html.Div(
        [
            html.H2("Hello.", className="text-center my-4"),
            dbc.Nav(
                [
                    dbc.NavLink([html.I(className="fas fa-house-user fa-lg m-3"), "Home"], active="exact",
                                href="home", className="custom-navlink"),
                    dbc.NavLink([html.I(className="fas fa-laptop fa-lg m-3"), "Device"], active="exact",
                                href="device", className="custom-navlink"),
                    dbc.NavLink([html.I(className="fas fa-chart-line fa-lg m-3"), "Dashboard"], active="exact",
                                href="dashboard", className="custom-navlink"),
                    dbc.NavLink([html.I(className="fas fa-tachometer-alt fa-lg m-3"), "Projects"], active="exact",
                                href="projects", className="custom-navlink"),
                ],
                vertical=True,
                pills=True,
            ),

        ], style={"height": "100vh"}
    )
