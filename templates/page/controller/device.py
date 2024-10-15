from dash.exceptions import PreventUpdate

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import requests
import json
from datetime import datetime

from ..layout.content.device.device_detail import *
from ..layout.content.device.device_edit import *
from ..layout.content.device.device import device_item

with open('config/server.json', 'r') as f:
    server = json.load(f)


def convert_bool_to_on_off(value):
    if value:
        return 'active'
    return 'inactive'


def device_controller(app):
    @app.callback(
        [Output('device-rows', 'children')],
        Input('url', 'pathname'),
    )
    def set_device_list_row(pathname):
        if pathname == '/beha-pulse/main/device/':
            user_id = session.get('user_id')  # 세션에서 user_id를 가져옴

            # 장치 정보를 저장할 리스트 초기화
            device_rows = []

            # 유저 장치 목록과 세부 정보를 한 번에 가져오는 API 호출
            api_url = f"http://{server['server']['host']}:{server['server']['port']}/user_device/user_devices_with_details/{user_id}"

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
                    device_rows.append(html.Div([]))

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
        Output('device-detail', 'href', allow_duplicate=True),
        Input('device-detail-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_device_list(n_clicks):
        if n_clicks:
            return "/beha-pulse/main/device/"

    @app.callback(
        Output('device-detail-main-content', 'children'),
        Input('url', 'pathname'),
    )
    def set_device_detail(pathname):
        if pathname == '/beha-pulse/main/device/detail/':
            mac_address = session['selected_device_mac_address']
            api_url = f"http://{server['server']['host']}:{server['server']['port']}/device/{mac_address}"
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    device = response.json().get('device', {})

                    # 상태를 ON/OFF에 따라 색상 변경 적용
                    on_off_status = 'ON' if device.get('on_off') else 'OFF'

                    return [
                        info_row('ic-manufacturing', '장치', device.get('type', 'N/A')),
                        info_row('ic-computer', 'MAC 주소', device.get('macAddress', 'N/A')),
                        info_row('ic-local-hospital', '설치 장소', device.get('install_location', 'N/A')),
                        info_row('ic-location-on', '설치 위치', device.get('room', 'N/A')),
                        info_row('ic-calendar-month', '점검 날짜', device.get('check_date', 'N/A')),
                        info_row('ic-offline-bolt', '상태', on_off_status, status=on_off_status),
                        info_row('ic-display-settings', '노트', device.get('note', 'N/A')),
                        info_row('ic-person-device', '사용자', '')
                    ]
                else:
                    return html.Div([])
            except requests.exceptions.RequestException as e:
                # 요청 예외 발생 시 처리
                return html.Div(f"RequestException occurred: {e}")
        else:
            return no_update

    @app.callback(
        Output('device-edit', 'href'),
        Input('device-edit-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_device_list(n_clicks):
        if n_clicks:
            return "/beha-pulse/main/device/detail/"

    @app.callback(
        [Output('on-button', 'style'),
         Output('off-button', 'style')],
        [Input('on-button', 'n_clicks'),
         Input('off-button', 'n_clicks')],
        [State('on-button', 'style'), State('off-button', 'style')],
        prevent_initial_call=True
    )
    def on_off_style_change(on_clicks, off_clicks, on_style, off_style):
        ctx = callback_context
        if not ctx.triggered:
            return on_style, off_style

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'on-button':
            on_style['color'] = '#00D84F'
            off_style['color'] = 'black'
            on_style['font-weight'] = 'bold'
            off_style['font-weight'] = 'normal'
        elif button_id == 'off-button':
            on_style['color'] = 'black'
            off_style['color'] = '#E10000'
            on_style['font-weight'] = 'normal'
            off_style['font-weight'] = 'bold'

        return on_style, off_style

    @app.callback(
        Output('device-edit-main-content', 'children'),
        Input('url', 'pathname'),
    )
    def set_device_edit_value(pathname):
        if pathname == '/beha-pulse/main/device/edit/':
            mac_address = session['selected_device_mac_address']
            api_url = f"http://{server['server']['host']}:{server['server']['port']}/device/{mac_address}"
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    device = response.json().get('device', {})
                    on_off_status = 'ON' if device.get('on_off') else 'OFF'

                    if on_off_status == 'ON':
                        on_status_color = '#00D84F',
                        off_status_color = 'black'
                        on_status_weight = 'bold'
                        off_status_weight = 'normal'
                    else:
                        on_status_color = 'black'
                        off_status_color = '#E10000'
                        on_status_weight = 'normal'
                        off_status_weight = 'bold'

                    on_style = {
                        'cursor': 'pointer',
                        'color': on_status_color,
                        'font-size': '1rem',
                        'align-items': 'center',
                        'font-weight': on_status_weight
                    }
                    off_style = {
                        'cursor': 'pointer',
                        'color': off_status_color,
                        'font-size': '1rem',
                        'align-items': 'center',
                        'font-weight': off_status_weight
                    }

                    return [
                        edit_row('ic-manufacturing', '장치', device.get('type', 'N/A'), '장치'),
                        edit_row('ic-computer', 'MAC 주소', device.get('macAddress', 'N/A'), 'MAC 주소'),
                        edit_row('ic-local-hospital', '설치 장소', device.get('install_location', 'N/A'), '설치 장소'),
                        edit_row('ic-location-on', '설치 위치', device.get('room', 'N/A'), '설치 위치'),
                        edit_row('ic-calendar-month', '점검 날짜', device.get('check_date', 'N/A'), 'YYYY-MM-DD'),
                        edit_on_off('ic-offline-bolt', on_style, off_style),
                        edit_row('ic-display-settings', '노트', device.get('note', 'N/A'), '메모'),
                        edit_row('ic-person-device', '사용자', '', '사용자')
                    ]
                else:
                    return html.Div(f"Error fetching device details: {response.status_code}")
            except requests.exceptions.RequestException as e:
                # 요청 예외 발생 시 처리
                return html.Div(f"RequestException occurred: {e}")
        else:
            return no_update

    @app.callback(
        Output('device-edit', 'href', allow_duplicate=True),
        Input('device-edit-save-button', 'n_clicks'),
        [State('device-edit-input-장치', 'value'),
         State('device-edit-input-MAC 주소', 'value'),
         State('device-edit-input-설치 장소', 'value'),
         State('device-edit-input-설치 위치', 'value'),
         State('device-edit-input-점검 날짜', 'value'),
         State('on-button', 'style'),
         State('off-button', 'style'),
         State('device-edit-input-노트', 'value')],
        prevent_initial_call=True
    )
    def save_device_edit(n_clicks, device_type, mac_address, install_location, room, check_date, on_style, off_style,
                         note):
        if n_clicks:
            if not all([device_type]):
                return html.Div("Please fill out all required fields.")

            if on_style['color'] == '#00D84F':
                on_off = "1"
            else:
                on_off = "0"

            try:
                check_date = datetime.strptime(check_date, "%Y-%m-%d").date()
                check_date_str = check_date.isoformat()  # Convert to string in ISO format (YYYY-MM-DD)

            except ValueError:
                raise no_update

            data = {
                'type': device_type,
                'macAddress': mac_address,
                'install_location': install_location,
                'room': room,
                'check_date': check_date_str,
                'on_off': on_off,
                'note': note
            }

            mac_address = session['selected_device_mac_address']
            api_url = f"http://{server['server']['host']}:{server['server']['port']}/device/update/{mac_address}"
            try:
                response = requests.put(api_url, json=data)
                if response.status_code == 200:
                    return "/beha-pulse/main/device/detail/"
                else:
                    return no_update
            except requests.exceptions.RequestException as e:
                # 요청 예외 발생 시 처리
                return no_update
        else:
            return no_update

    @app.callback(
        Output('device-detail', 'href', allow_duplicate=True),
        Input('device-delete-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def delete_device(n_clicks):
        if n_clicks:
            mac_address = session['selected_device_mac_address']
            api_url = f"http://{server['server']['host']}:{server['server']['port']}/device/delete/{mac_address}"
            try:
                response = requests.delete(api_url)
                if response.status_code == 200:
                    return "/beha-pulse/main/device/"
                else:
                    return no_update
            except requests.exceptions.RequestException as e:
                # 요청 예외 발생 시 처리
                return no_update
        else:
            return no_update

    @app.callback(
        Output('device-add', 'href'),
        Input('device-add-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_device_list(n_clicks):
        if n_clicks:
            return "/beha-pulse/main/device/"

    @app.callback(
        Output('device-add', 'href', allow_duplicate=True),
        Input('device-add-save-button', 'n_clicks'),
        [State('device-add-input-장치', 'value'),
         State('device-add-input-MAC 주소', 'value'),
         State('device-add-input-설치 장소', 'value'),
         State('device-add-input-설치 위치', 'value'),
         State('device-add-input-점검 날짜', 'value'),
         State('on-button', 'style'),
         State('off-button', 'style'),
         State('device-add-input-노트', 'value')],
        prevent_initial_call=True
    )
    def save_device_add(n_clicks, device_type, mac_address, install_location, room, check_date, on_style, off_style,
                        note):
        if n_clicks:
            if not all([device_type]):
                return html.Div("Please fill out all required fields.")

            if on_style['color'] == '#00D84F':
                on_off = "1"
            else:
                on_off = "0"

            try:
                check_date = datetime.strptime(check_date, "%Y-%m-%d").date()
                check_date_str = check_date.isoformat()  # Convert to string in ISO format (YYYY-MM-DD)

            except ValueError:
                raise no_update

            data = {
                'type': device_type,
                'macAddress': mac_address,
                'install_location': install_location,
                'room': room,
                'check_date': check_date_str,
                'on_off': on_off,
                'note': note
            }
            print(data)

            api_url = f"http://{server['server']['host']}:{server['server']['port']}/device/register"
            try:
                response = requests.post(api_url, json=data)
                if response.status_code == 200:
                    user_device_api_url = f"http://{server['server']['host']}:{server['server']['port']}/user_device/register"
                    user_device_data = {
                        'userEmail': session.get('user_id'),
                        'macAddress': mac_address
                    }
                    user_device_response = requests.post(user_device_api_url, json=user_device_data)
                    if user_device_response.status_code == 200:
                        return "/beha-pulse/main/device/"
                    else:
                        return no_update
                else:
                    return no_update
            except requests.exceptions.RequestException as e:
                # 요청 예외 발생 시 처리
                return no_update
        else:
            return no_update
