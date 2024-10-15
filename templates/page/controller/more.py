from dash.exceptions import PreventUpdate

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import requests
import json
from datetime import datetime

from ..layout.content.more.more_help import get_step_content

with open('config/server.json', 'r') as f:
    server = json.load(f)


def more_controller(app):
    @app.callback(
        Output('more', 'pathname'),
        [Input({'type': 'more-item', 'index': '개인정보 방침 조항'}, 'n_clicks'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def redirect_to_privacy_policy(n_clicks, pathname):
        if n_clicks:
            return '/beha-pulse/main/more/privacy-policy/'
        return pathname

    @app.callback(
        Output('more', 'pathname', allow_duplicate=True),
        [Input({'type': 'more-item', 'index': '이용약관'}, 'n_clicks'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def redirect_to_privacy_policy(n_clicks, pathname):
        if n_clicks:
            return '/beha-pulse/main/more/document/'
        return pathname

    @app.callback(
        Output('more', 'pathname', allow_duplicate=True),
        [Input({'type': 'more-item', 'index': '앱 정보'}, 'n_clicks'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def redirect_to_privacy_policy(n_clicks, pathname):
        if n_clicks:
            return '/beha-pulse/main/more/information/'
        return pathname

    @app.callback(
        Output('more', 'pathname', allow_duplicate=True),
        [Input({'type': 'more-item', 'index': '도움말'}, 'n_clicks'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def redirect_to_privacy_policy(n_clicks, pathname):
        if n_clicks:
            return '/beha-pulse/main/more/help/'
        return pathname

    @app.callback(
        [Output('more-overlay-background', 'style', allow_duplicate=True),
         Output('more-overlay-container', 'style', allow_duplicate=True)],
        [Input({'type': 'more-item', 'index': '로그아웃'}, 'n_clicks'),
         Input('more-overlay-background', 'n_clicks'),
         ],
        [State('more-overlay-background', 'style'),
         State('more-overlay-container', 'style')],
        prevent_initial_call=True
    )
    def loggout_overlay(n_clicks_button, n_clicks_background, background_style, container_style):
        ctx = callback_context
        if not ctx.triggered:
            return background_style, container_style

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Triggered ID를 딕셔너리로 변환
        try:
            triggered_dict = json.loads(triggered_id)
        except json.JSONDecodeError:
            triggered_dict = {}

        # 로그아웃 버튼 클릭 시 오버레이 열기
        if triggered_dict.get('index') == '로그아웃' and triggered_dict.get('type') == 'more-item' and n_clicks_button:
            background_style['display'] = 'block'
            container_style['display'] = 'block'

        # 오버레이 클릭으로 닫기
        elif triggered_id == 'more-overlay-background' and n_clicks_background:
            background_style['display'] = 'none'
            container_style['display'] = 'none'

        return background_style, container_style

    @app.callback(
        [Output('more-overlay-background', 'style', allow_duplicate=True),
         Output('more-overlay-container', 'style', allow_duplicate=True),
         Input('more-cancel-button', 'n_clicks')],
        [State('more-overlay-background', 'style'),
         State('more-overlay-container', 'style')],
        prevent_initial_call=True
    )
    def cancel_delete(n_clicks, background_style, container_style):
        if n_clicks:
            background_style['display'] = 'none'
            container_style['display'] = 'none'
        return background_style, container_style

    @app.callback(
        [Output('more-id', 'children'),
         Output('more-name', 'children')],
        Input('url', 'pathname'),
    )
    def set_more_id(pathname):
        if pathname == '/beha-pulse/main/more/':
            return session['user_id'], session['user_name']

    # 로그아웃 구현
    @app.callback(
        Output('redirect', 'href', allow_duplicate=True),
        Input('more-confirm-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def logout(n_clicks):
        if n_clicks:
            session.clear()
            return '/beha-pulse/login/'
        return no_update

    @app.callback(
        Output('redirect', 'href', allow_duplicate=True),
        Input('more-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_more(n_clicks):
        if n_clicks:
            return '/beha-pulse/main/more/'
        return no_update

    @app.callback(
        Output('more-help-current-step-store', 'data'),
        Input('more-help-next-button', 'n_clicks'),
        State('more-help-current-step-store', 'data'),
        prevent_initial_call=True
    )
    def next_step(n_clicks, current_step):
        if n_clicks:
            return current_step + 1
        return current_step

    @app.callback(
        [Output('more-help-main-content', 'children'),
         Output('redirect', 'href', allow_duplicate=True)],
        Input('more-help-current-step-store', 'data'),
        prevent_initial_call=True
    )
    def update_step(step):
        if step <= 3:
            return get_step_content(step), no_update
        else:
            return '', '/beha-pulse/main/more/'
