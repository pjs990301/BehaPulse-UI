from dash.exceptions import PreventUpdate

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import requests

from ..layout.content.device.device import *


def convert_bool_to_on_off(value):
    if value:
        return 'active'
    return 'inactive'


def device_controller(app):
    @app.callback(
        [Output('device-rows', 'children')],
        Input('main-url', 'pathname'),
    )

    def set_device_list_row(pathname):
        if pathname == '/beha-pulse/main/device/':
            user_id = session.get('user_id')  # 세션에서 user_id를 가져옴

            # 장치 정보를 저장할 리스트 초기화
            device_rows = []

            # 유저 장치 목록과 세부 정보를 한 번에 가져오는 API 호출
            api_url = f"http://192.9.200.141:8000/user_device/user_devices_with_details/{user_id}"

            try:
                # API 호출
                response = requests.get(api_url)
                if response.status_code == 200:
                    device_list = response.json().get('user_devices', [])

                    # 각 장치 정보를 기반으로 UI 구성
                    for device in device_list:
                        device_rows.append(device_item(
                            device.get('type', 'Unknown'),
                            device.get('macAddress', 'Unknown'),
                            convert_bool_to_on_off(device.get('on_off', 'inactive'))
                        ))

                else:
                    # API 호출 실패 시 에러 메시지 추가
                    device_rows.append(html.Div(f"Error fetching user devices: {response.status_code}"))

            except requests.exceptions.RequestException as e:
                # API 호출 중 예외 발생 시 처리
                device_rows.append(html.Div("RequestException occurred"))

            # 성공적으로 데이터를 처리한 경우 반환
            return [html.Div(device_rows)]

        # URL이 '/beha-pulse/main/device/'가 아닌 경우 업데이트하지 않음
        return no_update

    @app.callback(
        Output('device', 'href'),  # 출력은 화면에 표시되지 않음
        Input({'type': 'device-row', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def device_row_click(n_clicks):
        ctx = callback_context

        # index 중에서 클릭이 발생했을 때에만
        if not ctx.triggered or not n_clicks or all(click is None or click == 0 for click in n_clicks):
            raise PreventUpdate

        clicked_id = None
        for i, click in enumerate(n_clicks):
            if click and i < len(ctx.inputs_list[0]):  # 인덱스 범위 내에서 참조
                clicked_id = ctx.inputs_list[0][i]['id']['index']
                break

        if not clicked_id:
            raise PreventUpdate

        if clicked_id:
            session['selected_device_mac_address'] = clicked_id
            return '/beha-pulse/main/device/detail/'
        else:
            raise PreventUpdate

    @app.callback(
        Output('device-detail-url', 'href'),
        Input('device-detail-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_device_list(n_clicks):
        if n_clicks:
            return "/beha-pulse/main/"

    # @app.callback(
    #     Output('device-detail-main-content', 'children'),
    #     Input('device-detail-url', 'pathname'),
    #     prevent_initial_call=True
    # )
    # def set_device_detail(pathname):
    #     if pathname == '/beha-pulse/main/device/detail/':
    #         if 'selected_device_mac_address' in session:
    #             mac_address = session['selected_device_mac_address']
    #             api_url = f"http://