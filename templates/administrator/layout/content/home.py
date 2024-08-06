from flask import Flask
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def home_layout():
    return html.Div(
        dbc.Container([
            dbc.Row(
                [
                    dbc.Col(
                        html.H2("즐겨찾기", className=""),
                    ),
                ],
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader('Card Title'),
                        dbc.CardBody([
                            html.H5('Card Title', className='card-title'),
                            html.P('This is an example of a card with Dash Bootstrap Components.',
                                   className='card-text')
                        ])
                    ]),
                    width=3
                ),
                # justify='center'
            )
        ],
            className="mt-3 mx-3")
    )
