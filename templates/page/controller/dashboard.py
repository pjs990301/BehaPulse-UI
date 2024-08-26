from dash.exceptions import PreventUpdate
from datetime import datetime

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import requests
import requests

from ..layout.content.dashboard import create_dashboard_card
from ..layout.content.dashboard_person_info import create_person_detail_row
from ..layout.content.dashboard_person_edit import create_person_edit_row


def dashboard_controller(app):
    @app.callback(
        Output('dashboard-cards-row', 'children'),
        [Input('url', 'pathname')]
    )
    def render_device_card(pathname):
        if pathname == '/admin/dashboard':
            user_email = session.get('user_email')

            api_url = f"http://192.9.200.141:8000/user_dashboard/user_dashboards/{user_email}"

            try:
                response = requests.get(api_url)

                if response.status_code == 200:
                    user_dashboards = response.json().get('dashboards', [])
                    cards = []

                    for dashboard in user_dashboards:
                        person_id = dashboard[1]
                        dashboard_api_url = f"http://192.9.200.141:8000/dashboard/{person_id}"
                        try:
                            dashboard_response = requests.get(dashboard_api_url)
                            if dashboard_response.status_code == 200:
                                dashboard_data = dashboard_response.json().get('dashboard', {})
                                cards.append(create_dashboard_card(
                                    dashboard_data.get('personId', 'Unknown'),
                                    dashboard_data.get('name', 'Unknown'),
                                    dashboard_data.get('gender', 'Unknown'),
                                    dashboard_data.get('birth', 'Unknown'),
                                    dashboard_data.get('status', 'Unknown')
                                ))
                            else:
                                cards.append(
                                    create_dashboard_card(person_id, 'Unknown', 'Unknown', 'Unknown', 'Unknown'))
                        except requests.exceptions.RequestException as e:
                            cards.append(
                                create_dashboard_card(person_id, 'Unknown', 'Unknown', 'Unknown', 'Unknown'))

                    return cards

                else:
                    return [create_dashboard_card(0, 'Unknown', 'Unknown', 'Unknown', 'Unknown')]

            except requests.exceptions.RequestException as e:
                return [create_dashboard_card(0, 'Unknown', 'Unknown', 'Unknown', 'Unknown')]

    @app.callback(
        Output('url', 'pathname', allow_duplicate=True),
        Input({'type': 'dashboard-dots-icon', 'index': ALL}, 'n_clicks'),  # Input comes after Outputs,
        prevent_initial_call=True

    )
    def store_clicked_person(n_clicks):
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
            session['selected_dashboard_id'] = clicked_id
            return '/admin/dashboard/detail'
        else:
            raise PreventUpdate

    @app.callback(
        Output('person-detail-row', 'children'),
        [Input('url', 'pathname')]
    )
    def render_device_detail(pathname):
        if pathname == '/admin/dashboard/detail/info':
            person_id = session.get('selected_dashboard_id')
            api_url = f"http://192.9.200.141:8000/dashboard/{person_id}"
            detail_row = []
            try:
                response = requests.get(api_url)

                if response.status_code == 200:
                    person_data = response.json().get('dashboard', {})
                    # Redirect to the detail page and pass device data
                    detail_row.append(create_person_detail_row("성명", person_data.get('name', 'Unknown Person'))),
                    detail_row.append(create_person_detail_row("성별", person_data.get('gender', 'Unknown Person'))),
                    detail_row.append(create_person_detail_row("생년월일", person_data.get('birth', 'Unknown Person'))),
                    detail_row.append(create_person_detail_row("위치", person_data.get('location', 'Unknown Person'))),

                    return detail_row
                else:
                    return detail_row.append(create_person_detail_row("No Unknown found", "Unknown Person"))
            except requests.exceptions.RequestException as e:
                return detail_row.append(create_person_detail_row("No Unknown found", "Unknown Person"))
        else:
            # update 하지 않기
            raise PreventUpdate

    @app.callback(
        Output('dashboard-detail-edit-row', 'children'),
        [Input('url', 'pathname')],

    )
    def render_dashboard_edit(pathname):
        if pathname == '/admin/dashboard/detail/edit':
            person_id = session.get('selected_dashboard_id')
            api_url = f"http://192.9.200.141:8000/dashboard/{person_id}"
            edit_row = []
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    person_data = response.json().get('dashboard', {})
                    # Redirect to the detail page and pass device data
                    edit_row.append(create_person_edit_row("성명", person_data.get('name', 'Unknown Person'))),
                    edit_row.append(
                        create_person_edit_row("성별", person_data.get('gender', 'Unknown Person'))),
                    edit_row.append(create_person_edit_row("생년월일", person_data.get('birth', 'Unknown Person'))),
                    edit_row.append(create_person_edit_row("위치", person_data.get('location', 'Unknown Person'))),

                    return edit_row
                else:
                    return edit_row.append(create_person_edit_row("No Unknown found", "Unknown Person"))
            except requests.exceptions.RequestException as e:
                return edit_row.append(create_person_edit_row("No Unknown found", "Unknown Person"))

        else:
            # update 하지 않기
            raise PreventUpdate

    @app.callback(
        Output('hidden-div-dashboard-edit', 'children'),  # Using a dummy output

        Input('dashboard-edit-save-button', 'n_clicks'),
        [
            State('dashboard-edit-성명', 'value'),
            State('dashboard-edit-성별', 'value'),
            State('dashboard-edit-생년월일', 'value'),
            State('dashboard-edit-위치', 'value'),
        ],
        prevent_initial_call=True
    )
    def save_device_edit(n_clicks, name, gender, birth, location):
        if n_clicks is None or n_clicks == 0:
            return PreventUpdate
        # else:
        #     print("Button clicked")

        # Validate State values
        if not all([name, gender, birth, location]):
            # print("Missing state values. Preventing update.")
            raise PreventUpdate

        ctx = callback_context
        # print("Triggered:", ctx.triggered)

        if not ctx.triggered:
            raise PreventUpdate
        try:
            check_date = datetime.strptime(birth, "%Y-%m-%d").date()
            check_date_str = check_date.isoformat()  # Convert to string in ISO format (YYYY-MM-DD)
        except ValueError:
            raise PreventUpdate

        api_url = f"http://192.9.200.141:8000/dashboard/update/{session.get('selected_dashboard_id')}"
        data = {
            "name": name,
            "gender": gender,
            "birth": check_date_str,
            "location": location
        }

        try:
            response = requests.put(api_url, json=data)
            if response.status_code == 200:
                return html.Div("저장 성공")
            elif response.status_code == 404:
                return html.Div("해당 디바이스를 찾을 수 없습니다.")
            else:
                return html.Div("서버 연결 실패")
        except requests.exceptions.RequestException as e:
            return html.Div(f"An error occurred: {str(e)}")

    @app.callback(
        Output('hidden-div-dashboard-delete', 'children'),  # Using a dummy output
        Input('dashboard-edit-delete-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def delete_device(n_clicks):
        if n_clicks is None or n_clicks == 0:
            return PreventUpdate

        person_id = session.get('selected_dashboard_id')
        api_url = f"http://192.9.200.141:8000/dashboard/{person_id}"
        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                person_data = response.json().get('dashboard', {})
                person_name = person_data.get('name', 'Unknown Person')

                api_url = f"http://192.9.200.141:8000/dashboard/delete/{person_id}/{person_name}"

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
            else:
                return html.Div("해당 디바이스를 찾을 수 없습니다.")
        except requests.exceptions.RequestException as e:
            return html.Div(f"An error occurred: {str(e)}")

    @app.callback(
        Output('hidden-div-dashboard-add', 'children'),  # Using a dummy output
        Input('dashboard-add-save-button', 'n_clicks'),
        [
            State('dashboard-add-성명', 'value'),
            State('dashboard-add-성별', 'value'),
            State('dashboard-add-생년월일', 'value'),
            State('dashboard-add-위치', 'value'),
        ],
        prevent_initial_call=True
    )
    def save_dashboard_add(n_clicks, name, gender, birth, location):
        if n_clicks is None or n_clicks == 0:
            return PreventUpdate
        # else:
        #     print("Button clicked")

        # Validate State values
        if not all([name, gender, birth, location]):
            # print("Missing state values. Preventing update.")
            raise PreventUpdate

        ctx = callback_context
        # print("Triggered:", ctx.triggered)

        if not ctx.triggered:
            raise PreventUpdate
        try:
            check_date = datetime.strptime(birth, "%Y-%m-%d").date()
            check_date_str = check_date.isoformat()  # Convert to string in ISO format (YYYY-MM-DD)
        except ValueError:
            raise PreventUpdate

        api_url = f"http://192.9.200.141:8000/dashboard/register"
        data = {
            "name": name,
            "gender": gender,
            "birth": check_date_str,
            "location": location
        }

        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 200:
                # 저장하고 user_device에도 등록
                user_email = session.get('user_email')
                person_id = response.json()['personId']

                user_dashboard_api_url = f"http://192.9.200.141:8000/user_dashboard/register"
                user_dashboard_data = {
                    "userEmail": user_email,
                    "personId": person_id
                }
                user_device_response = requests.post(user_dashboard_api_url, json=user_dashboard_data)
                if user_device_response.status_code == 200:
                    return html.Div("저장 성공")
            elif response.status_code == 404:
                return html.Div("해당 디바이스를 찾을 수 없습니다.")
            else:
                return html.Div("서버 연결 실패")
        except requests.exceptions.RequestException as e:
            return html.Div(f"An error occurred: {str(e)}")
        return html.Div("저장 성공")

    @app.callback(
        [Output('dashboard-detail-name', 'children'),
         Output('dashboard-detail-date', 'children')],
        [Input('url', 'pathname')]
    )
    def render_dashboard_detail_name(pathname):
        if pathname == '/admin/dashboard/detail':
            person_id = session.get('selected_dashboard_id')
            api_url = f"http://192.9.200.141:8000/dashboard/{person_id}"
            try:
                response = requests.get(api_url)

                if response.status_code == 200:
                    person_data = response.json().get('dashboard', {})
                    person_name = person_data.get('name', 'Unknown Person')
                    current_time = datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")
                    return person_name, current_time
                else:
                    return "Unknown Person", "0000년 00월 00일 00:00:00"
            except requests.exceptions.RequestException as e:
                return "Unknown Person", "0000년 00월 00일 00:00:00"
        else:
            raise PreventUpdate
