from dash.exceptions import PreventUpdate
from datetime import datetime

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import requests
from ..layout.content.device import create_device_card
from ..layout.content.device_detail import create_detail_row
from ..layout.content.device_edit import create_detail_edit_row, create_detail_on_off
from ..layout.content.device_add import create_detail_row_add, create_detail_on_off


def convert_bool_to_on_off(value):
    if value:
        return 'on'
    return 'off'


def device_controller(app):
    @app.callback(
        [Output('on-button', 'style'),
         Output('off-button', 'style')],
        [Input('on-button', 'n_clicks'),
         Input('off-button', 'n_clicks')],
        [State('on-button', 'style'), State('off-button', 'style')]
    )
    def toggle_buttons(on_clicks, off_clicks, on_style, off_style):
        ctx = callback_context
        if not ctx.triggered:
            return on_style, off_style

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'on-button':
            on_style['color'] = '#00FF5D'
            off_style['color'] = 'white'
        elif button_id == 'off-button':
            on_style['color'] = 'white'
            off_style['color'] = '#E50C0C'

        return on_style, off_style

    @app.callback(
        Output('device-cards-row', 'children'),
        [Input('url', 'pathname')]
    )
    def render_device_card(pathname):
        if pathname == '/admin/device':
            user_email = session.get('user_email')

            api_url = f"http://192.9.200.141:8000/user_device/user_devices/{user_email}"

            try:
                response = requests.get(api_url)

                if response.status_code == 200:
                    user_devices = response.json().get('user_devices', [])
                    cards = []  # 여기에 생성된 카드들을 담을 리스트를 생성합니다.
                    for device in user_devices:
                        user_device_id = device[2]
                        device_api_url = f"http://192.9.200.141:8000/device/{user_device_id}"
                        try:
                            device_response = requests.get(device_api_url)

                            if device_response.status_code == 200:
                                device_data = device_response.json().get('device', {})
                                cards.append(create_device_card(
                                    device_data.get('type', 'Unknown Device'),
                                    device_data.get('macAddress', 'Unknown MAC'),
                                    convert_bool_to_on_off(device_data.get('on_off', 'off'))
                                ))
                            else:
                                # cards.append(create_device_card("No devices found", "Unknown MAC", "off"))
                                cards.append([])
                        except requests.exceptions.RequestException as e:
                            # cards.append(create_device_card("No devices found", "Unknown MAC", "off"))
                            cards.append([])
                    return cards  # 리스트로 반환

                else:
                    return []
                    # return [create_device_card("No devices found", "Unknown MAC", "off")]

            except requests.exceptions.RequestException as e:
                return []
                # return [create_device_card("No devices found", "Unknown MAC", "off")]

    @app.callback(
        Output('url', 'pathname', allow_duplicate=True),
        Input({'type': 'device-dots-icon', 'index': ALL}, 'n_clicks'),  # Input comes after Outputs,
        prevent_initial_call=True

    )
    def store_clicked_mac(n_clicks):
        ctx = callback_context

        if not ctx.triggered or not n_clicks or all(click is None or click == 0 for click in n_clicks):
            raise PreventUpdate
        # 안전한 인덱스 참조를 위해 리스트 길이 확인
        clicked_id = None
        for i, click in enumerate(n_clicks):
            if click and i < len(ctx.inputs_list[0]):  # 인덱스 범위 내에서 참조
                clicked_id = ctx.inputs_list[0][i]['id']['index']
                break

        if not clicked_id:
            raise PreventUpdate

        if clicked_id:
            session['selected_device_mac_address'] = clicked_id
            return '/admin/device/detail'
        else:
            raise PreventUpdate

    @app.callback(
        Output('device-edit-person-dropdown', 'options'),
        [Input('url', 'pathname'),
         Input('device-edit-person-dropdown', 'search_value')]
    )
    def render_dropdown_detail(pathname, search_value):
        if pathname == '/admin/device/edit':
            user_email = session.get('user_email')
            api_url = f"http://192.9.200.141:8000/user_dashboard/user_dashboards/{user_email}"

            try:
                response = requests.get(api_url)

                if response.status_code == 200:
                    user_dashboards = response.json().get('dashboards', [])
                    dropdown_options = []

                    for dashboard in user_dashboards:
                        person_id = dashboard[1]
                        dashboard_api_url = f"http://192.9.200.141:8000/dashboard/{person_id}"

                        try:
                            dashboard_response = requests.get(dashboard_api_url)
                            if dashboard_response.status_code == 200:
                                dashboard_data = dashboard_response.json().get('dashboard', {})
                                user_name = dashboard_data.get('name', 'Unknown Person')
                                dropdown_options.append({'label': user_name, 'value': person_id})

                        except requests.RequestException as e:
                            print(f"Error fetching dashboard data: {e}")

                    return dropdown_options

                else:
                    print(f"Failed to fetch user dashboards: {response.status_code}")
                    return []

            except requests.RequestException as e:
                print(f"Error fetching user dashboards: {e}")
                return []

        # 빈 옵션 리스트 반환
        return []

    @app.callback(
        Output('device-add-person-dropdown', 'options'),
        [Input('url', 'pathname'),
         Input('device-add-person-dropdown', 'search_value')]
    )
    def render_dropdown_add_detail(pathname, search_value):
        if pathname == '/admin/device/add':
            user_email = session.get('user_email')
            api_url = f"http://192.9.200.141:8000/user_dashboard/user_dashboards/{user_email}"

            try:
                response = requests.get(api_url)

                if response.status_code == 200:
                    user_dashboards = response.json().get('dashboards', [])
                    dropdown_options = []

                    for dashboard in user_dashboards:
                        person_id = dashboard[1]
                        dashboard_api_url = f"http://192.9.200.141:8000/dashboard/{person_id}"

                        try:
                            dashboard_response = requests.get(dashboard_api_url)
                            if dashboard_response.status_code == 200:
                                dashboard_data = dashboard_response.json().get('dashboard', {})
                                user_name = dashboard_data.get('name', 'Unknown Person')
                                dropdown_options.append({'label': user_name, 'value': person_id})

                        except requests.RequestException as e:
                            print(f"Error fetching dashboard data: {e}")

                    return dropdown_options

                else:
                    print(f"Failed to fetch user dashboards: {response.status_code}")
                    return []

            except requests.RequestException as e:
                print(f"Error fetching user dashboards: {e}")
                return []

        # 빈 옵션 리스트 반환
        return []

    @app.callback(
        Output('device-detail-row', 'children'),
        [Input('url', 'pathname')]
    )
    def render_device_detail(pathname):
        if pathname == '/admin/device/detail':
            mac_address = session.get('selected_device_mac_address')
            api_url = f"http://192.9.200.141:8000/device/{mac_address}"
            detail_row = []
            try:
                response = requests.get(api_url)

                if response.status_code == 200:
                    device_data = response.json().get('device', {})
                    # Redirect to the detail page and pass device data
                    detail_row.append(create_detail_row("장치명", device_data.get('type', 'Unknown Device'))),
                    detail_row.append(create_detail_row("Mac 주소", device_data.get('macAddress', "00:00:00:00:00:00"))),
                    detail_row.append(create_detail_row("설치 장소", device_data.get('install_location', ""))),
                    detail_row.append(create_detail_row("호실", device_data.get('room', ""))),
                    detail_row.append(create_detail_row("점검일", device_data.get('check_date', "00년 00월 00일"))),
                    detail_row.append(
                        create_detail_row("활성화 상태", convert_bool_to_on_off(device_data.get('on_off', "off")))),
                    detail_row.append(create_detail_row("기타사항", device_data.get('note', ""))),

                    device_id = device_data.get('deviceId', 0)
                    if device_id != 0:
                        user_email = session.get('user_email')
                        find_person_url = f"http://192.9.200.141:8000/user_dashboard_device/user_dashboard_devices/{user_email}/{device_id}"
                        try:
                            response = requests.get(find_person_url)
                            if response.status_code == 200:
                                person_data = response.json().get('user_dashboard_device', {})
                                person_id = person_data[2]
                                find_person_name_url = f"http://192.9.200.141:8000/dashboard/{person_id}"
                                try:
                                    response = requests.get(find_person_name_url)
                                    if response.status_code == 200:
                                        person_name = response.json().get('dashboard', {}).get('name', 'Unknown Person')
                                        detail_row.append(create_detail_row("사용자", person_name))
                                    else:
                                        detail_row.append(create_detail_row("사용자", ""))
                                except requests.exceptions.RequestException as e:
                                    detail_row.append(create_detail_row("사용자", ""))
                            else:
                                detail_row.append(create_detail_row("사용자", ""))
                        except requests.exceptions.RequestException as e:
                            detail_row.append(create_detail_row("사용자", ""))
                    else:
                        detail_row.append(create_detail_row("사용자", ""))

                    return detail_row
                else:
                    # return detail_row.append(create_detail_row("No device found", "Unknown Device"))
                    return detail_row.append([])
            except requests.exceptions.RequestException as e:
                # return detail_row.append(create_detail_row("No device found", "Unknown Device"))
                return detail_row.append([])
        else:
            # update 하지 않기
            raise PreventUpdate

    @app.callback(
        Output('device-detail-edit-row', 'children'),
        [Input('url', 'pathname')],

    )
    def render_device_edit(pathname):
        if pathname == '/admin/device/edit':
            mac_address = session.get('selected_device_mac_address')
            api_url = f"http://192.9.200.141:8000/device/{mac_address}"
            edit_row = []
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    device_data = response.json().get('device', {})
                    # Redirect to the detail page and pass device data
                    edit_row.append(create_detail_edit_row("장치명", device_data.get('type', 'Unknown Device'))),
                    edit_row.append(
                        create_detail_edit_row("Mac 주소", device_data.get('macAddress', "00:00:00:00:00:00"))),
                    edit_row.append(create_detail_edit_row("설치 장소", device_data.get('install_location', ""))),
                    edit_row.append(create_detail_edit_row("호실", device_data.get('room', ""))),
                    edit_row.append(create_detail_edit_row("점검일", device_data.get('check_date', "00년 00월 00일"))),

                    on_off_status = convert_bool_to_on_off(device_data.get('on_off', 0))
                    if on_off_status == "on":
                        on_status_color = "#00FF5D"
                        off_status_color = "white"
                    else:
                        on_status_color = "white"
                        off_status_color = "#E50C0C"

                    # Define styles based on on_off status
                    # of_off 1: on, 0: off
                    on_style = {
                        'cursor': 'pointer',
                        'color': on_status_color,
                        'font-size': '1rem',
                        'padding': '0px 20px'
                    }
                    off_style = {
                        'cursor': 'pointer',
                        'color': off_status_color,
                        'font-size': '1rem',
                        'padding': '0px 20px'
                    }

                    edit_row.append(
                        edit_row.append(create_detail_on_off("활성화 상태", on_style, off_style)),
                    ),
                    edit_row.append(create_detail_edit_row("기타사항", device_data.get('note', ""))),
                    return edit_row
                else:
                    # return edit_row.append(create_detail_edit_row("No device found", "Unknown Device"))
                    return edit_row.append([])
            except requests.exceptions.RequestException as e:
                # return edit_row.append(create_detail_edit_row("No device found", "Unknown Device"))
                return edit_row.append([])

        else:
            # update 하지 않기
            raise PreventUpdate

    @app.callback(
        Output('hidden-div-device-edit', 'children'),  # Using a dummy output

        Input('device-edit-save-button', 'n_clicks'),
        [
            State('device-edit-장치명', 'value'),
            State('device-edit-Mac 주소', 'value'),
            State('device-edit-설치 장소', 'value'),
            State('device-edit-호실', 'value'),
            State('device-edit-점검일', 'value'),
            State('on-button', 'style'),
            State('off-button', 'style'),
            State('device-edit-기타사항', 'value'),
            State('device-edit-person-dropdown', 'value')
        ],
        prevent_initial_call=True
    )
    def save_device_edit(n_clicks, device_type, mac_address, install_location, room, check_date, on_style, off_style,
                         note, person_id):
        if n_clicks is None or n_clicks == 0:
            return PreventUpdate
        # else:
        #     print("Button clicked")

        # Validate State values
        if not all(
                [device_type, mac_address, install_location, room, check_date, on_style, off_style, note, person_id]):
            # print("Missing state values. Preventing update.")
            raise PreventUpdate

        # Validate that the button styles are provided
        if not on_style or not off_style:
            raise PreventUpdate

        ctx = callback_context
        # print("Triggered:", ctx.triggered)

        if not ctx.triggered:
            raise PreventUpdate

        on_button_color = on_style.get('color', 'white')
        off_button_color = off_style.get('color', 'white')

        if on_button_color.lower() != 'white':
            device_status = "1"  # 'on' as 1
        elif off_button_color.lower() != 'white':
            device_status = "0"  # 'off' as 0
        else:
            device_status = "0"
        # Convert check_date to a datetime.date object and then to a string
        try:
            check_date = datetime.strptime(check_date, "%Y-%m-%d").date()
            check_date_str = check_date.isoformat()  # Convert to string in ISO format (YYYY-MM-DD)
        except ValueError:
            raise PreventUpdate

        api_url = f"http://192.9.200.141:8000/device/update/{mac_address}"
        data = {
            "macAddress": mac_address,
            "type": device_type,
            "install_location": install_location,
            "room": room,
            "check_date": check_date_str,
            "on_off": device_status,
            "note": note
        }

        try:
            response = requests.put(api_url, json=data)
            if response.status_code == 200:
                find_device_url = f"http://192.9.200.141:8000/device/{mac_address}"
                find_device_response = requests.get(find_device_url)
                if find_device_response.status_code == 200:
                    device_data = find_device_response.json().get('device', {})
                    device_id = device_data.get('deviceId', 0)
                    if device_id != 0:
                        user_email = session.get('user_email')
                        user_device_api_url = f"http://192.9.200.141:8000/user_dashboard_device/update/{user_email}/{device_id}"
                        user_device_data = {
                            "userEmail": user_email,
                            "deviceId": device_id,
                            "personId": person_id
                        }
                        user_device_response = requests.put(user_device_api_url, json=user_device_data)
                        if user_device_response.status_code == 200:
                            return html.Div("저장 성공")
                    else:
                        return html.Div("해당 디바이스를 찾을 수 없습니다.")
                else:
                    return html.Div("해당 디바이스를 찾을 수 없습니다.")
            elif response.status_code == 404:
                return html.Div("해당 디바이스를 찾을 수 없습니다.")
            else:
                return html.Div("서버 연결 실패")
        except requests.exceptions.RequestException as e:
            return html.Div(f"An error occurred: {str(e)}")
        except Exception as e:
            return html.Div(f"An error occurred: {str(e)}")

    @app.callback(
        Output('hidden-div-device-add', 'children'),  # Using a dummy output

        Input('device-add-save-button', 'n_clicks'),
        [
            State('device-add-장치명', 'value'),
            State('device-add-Mac 주소', 'value'),
            State('device-add-설치 장소', 'value'),
            State('device-add-호실', 'value'),
            State('device-add-점검일', 'value'),
            State('on-button', 'style'),
            State('off-button', 'style'),
            State('device-add-기타사항', 'value'),
            State('device-add-person-dropdown', 'value')

        ],
        prevent_initial_call=True
    )
    def save_device_add(n_clicks, device_type, mac_address, install_location, room, check_date, on_style, off_style,
                        note, person_id):
        if n_clicks is None or n_clicks == 0:
            return PreventUpdate
        # else:
        #     print("Button clicked")

        # Validate State values
        if not all(
                [device_type, mac_address, install_location, room, check_date, on_style, off_style, note, person_id]):
            # print("Missing state values. Preventing update.")
            raise PreventUpdate

        # Validate that the button styles are provided
        if not on_style or not off_style:
            raise PreventUpdate

        ctx = callback_context
        # print("Triggered:", ctx.triggered)

        if not ctx.triggered:
            raise PreventUpdate

        on_button_color = on_style.get('color', 'white')
        off_button_color = off_style.get('color', 'white')

        if on_button_color.lower() != 'white':
            device_status = "1"  # 'on' as 1
        elif off_button_color.lower() != 'white':
            device_status = "0"  # 'off' as 0
        else:
            device_status = "0"
        # Convert check_date to a datetime.date object and then to a string
        try:
            check_date = datetime.strptime(check_date, "%Y-%m-%d").date()
            check_date_str = check_date.isoformat()  # Convert to string in ISO format (YYYY-MM-DD)
        except ValueError:
            raise PreventUpdate

        # print(device_type, mac_address, install_location, room, check_date_str, device_status, note)
        # print(type(device_type))
        # print(type(mac_address))
        # print(type(install_location))
        # print(type(room))
        # print(type(check_date_str))
        # print(type(device_status))
        # print(type(note))

        api_url = f"http://192.9.200.141:8000/device/register"
        data = {
            "macAddress": mac_address,
            "type": device_type,
            "install_location": install_location,
            "room": room,
            "check_date": check_date_str,
            "on_off": device_status,
            "note": note
        }

        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 200:
                # 저장하고 user_device에도 등록
                user_email = session.get('user_email')
                # print(user_email)
                # print(mac_address)
                user_device_api_url = f"http://192.9.200.141:8000/user_device/register"
                user_device_data = {
                    "userEmail": user_email,
                    "macAddress": mac_address
                }
                user_device_response = requests.post(user_device_api_url, json=user_device_data)
                if user_device_response.status_code == 200:
                    # deviceId 가져오기
                    find_device_url = f"http://192.9.200.141:8000/device/{mac_address}"
                    find_device_response = requests.get(find_device_url)
                    if find_device_response.status_code == 200:
                        device_data = find_device_response.json().get('device', {})
                        device_id = device_data.get('deviceId', 0)
                        if device_id != 0:
                            user_device_api_url = f"http://192.9.200.141:8000/user_dashboard_device/register"
                            user_device_data = {
                                "userEmail": user_email,
                                "deviceId": device_id,
                                "personId": person_id
                            }
                            user_device_response = requests.post(user_device_api_url, json=user_device_data)
                            if user_device_response.status_code == 200:
                                return html.Div("저장 성공")
                        else:
                            return html.Div("해당 디바이스를 찾을 수 없습니다.")
                    else:
                        return html.Div("해당 디바이스를 찾을 수 없습니다.")
                else:
                    return html.Div("서버 연결 실패")
            elif response.status_code == 404:
                return html.Div("해당 디바이스를 찾을 수 없습니다.")
            else:
                return html.Div("서버 연결 실패")
        except requests.exceptions.RequestException as e:
            return html.Div(f"An error occurred: {str(e)}")

    @app.callback(
        Output('hidden-div-device-delete', 'children'),  # Using a dummy output
        Input('device-edit-delete-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def delete_device(n_clicks):
        if n_clicks is None or n_clicks == 0:
            return PreventUpdate

        mac_address = session.get('selected_device_mac_address')
        api_url = f"http://192.9.200.141:8000/device/delete/{mac_address}"
        try:
            response = requests.delete(api_url)
            if response.status_code == 200:
                return html.Div("삭제 성공")
            elif response.status_code == 404:
                return html.Div("해당 디바이스를 찾을 수 없습니다.")
            else:
                return html.Div("서버 연결 실패")
        except requests.exceptions.RequestException as e:
            return html.Div(f"An error occurred: {str(e)}")
