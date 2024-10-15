from dash.exceptions import PreventUpdate

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import requests
import json
from datetime import datetime

from ..layout.content.dashboard.dashboard import *
from ..layout.content.dashboard.dashboard_add import *
from ..layout.content.dashboard.dashboard_delete import *

with open('config/server.json', 'r') as f:
    server = json.load(f)


def dashboard_controller(app):
    # 현재 단계에 따른 UI 업데이트
    @app.callback(
        [Output('dashboard-add-text-content', 'children'),
         Output('dashboard-add-main-content', 'children')],
        [Input('dashboard-add-current-step-store', 'data')],
    )
    def update_ui(step):
        # set Default value
        step = step if step else 1

        return get_step_content(step)

    @app.callback(
        Output('dashboard-rows', 'children'),
        Input('url', 'pathname')
    )
    def set_dashboard_list_row(pathname):
        print(pathname)
        if pathname == '/beha-pulse/main/dashboard/':
            user_id = session.get('user_id')

            dashboard_row = []

            api_url = f'http://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard/user_dashboards_with_details/{user_id}'

            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    dashboard_list = response.json().get('dashboards', [])
                    for dashboard in dashboard_list:
                        if dashboard['status'] is None:
                            dashboard['status'] = '확인불가'

                        dashboard_row.append(dashboard_item(
                            dashboard['personId'],
                            dashboard['name'],
                            dashboard['gender'],
                            dashboard['birth'],
                            dashboard['status']
                        ))
                else:
                    dashboard_row.append([])
            except Exception as e:
                dashboard_row.append([])

            return [html.Div(dashboard_row)]

        elif pathname == '/beha-pulse/main/dashboard/delete/':
            user_id = session.get('user_id')

            dashboard_row = []

            api_url = f'http://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard/user_dashboards_with_details/{user_id}'

            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    dashboard_list = response.json().get('dashboards', [])
                    for dashboard in dashboard_list:
                        if dashboard['status'] is None:
                            dashboard['status'] = '확인불가'

                        dashboard_row.append(dashboard_check_item(
                            dashboard['personId'],
                            dashboard['name'],
                            dashboard['gender'],
                            dashboard['birth'],
                            dashboard['status']
                        ))
                else:
                    dashboard_row.append([])
            except Exception as e:
                dashboard_row.append([])

            return [html.Div(dashboard_row)]

        return no_update

    app.clientside_callback(
        """
        function(n_clicks, step, dashboard_data) {
            const MAX_STEP = 4;  // 최대 단계 설정
            
            if (!n_clicks || step >= MAX_STEP) {
                return [dashboard_data, step];  // n_clicks가 없거나 최대 단계에 도달하면 현재 단계 유지
            }

            // Step에 따라 입력 필드에서 값 가져오기
            let nameInput = document.getElementById('dashboard-add-input-name');
            
            let manButton = document.getElementById('dashboard-add-input-gender-man');
            let womanButton = document.getElementById('dashboard-add-input-gender-woman');
            
            let yearInput = document.getElementById('dashboard-add-input-year');
            let monthInput = document.getElementById('dashboard-add-input-month');
            let dayInput = document.getElementById('dashboard-add-input-day');
            
            if (!dashboard_data) {
                dashboard_data = {};
            }

            // 단계별로 데이터를 저장하고 검사 후 버튼 상태 변경
            if (step === 1 && nameInput) {
                dashboard_data['name'] = nameInput.value;                
                if (!dashboard_data['name']) {
                    alert('이름을 입력해주세요.');
                    return [dashboard_data, step];
                }
                console.log("Name stored: " + dashboard_data['name']);

            }
            else if (step === 2 && yearInput && monthInput && dayInput) {
                // 입력값을 숫자로 변환
                dashboard_data['year'] = parseInt(yearInput.value, 10);
                dashboard_data['month'] = parseInt(monthInput.value, 10);
                dashboard_data['day'] = parseInt(dayInput.value, 10);
                
                // 값이 비어 있으면 경고
                if (!dashboard_data['year'] || !dashboard_data['month'] || !dashboard_data['day']) {
                    alert('생년월일을 입력해주세요.');
                    return [dashboard_data, step];
                }
            
                // 생년월일 유효성 검사
                if (dashboard_data['year'] < 1900 || dashboard_data['year'] > new Date().getFullYear()) {
                    alert('올바른 연도를 입력해주세요.');
                    yearInput.value = '';
                    return [dashboard_data, step];
                }
                if (dashboard_data['month'] < 1 || dashboard_data['month'] > 12) {
                    alert('올바른 월을 입력해주세요.');
                    monthInput.value = '';
                    return [dashboard_data, step];
                }
            
                // 각 달의 최대 일수 확인 함수
                function getDaysInMonth(year, month) {
                    return new Date(year, month, 0).getDate();  // 해당 월의 마지막 날짜 반환
                }
            
                // 입력된 월의 최대 일수 확인
                let maxDays = getDaysInMonth(dashboard_data['year'], dashboard_data['month']);
                if (dashboard_data['day'] < 1 || dashboard_data['day'] > maxDays) {
                    alert(`올바른 일을 입력해주세요. ${dashboard_data['month']}월은 ${maxDays}일까지 있습니다.`);
                    dayInput.value = '';
                    return [dashboard_data, step];
                }
            
                // 생년월일 입력 양식 확인 yyyy mm dd (한 자리수 월/일의 경우 0 추가)
                dashboard_data['month'] = dashboard_data['month'] < 10 ? '0' + dashboard_data['month'] : dashboard_data['month'].toString();
                dashboard_data['day'] = dashboard_data['day'] < 10 ? '0' + dashboard_data['day'] : dashboard_data['day'].toString();
            
                console.log("Year stored: " + dashboard_data['year']);
                console.log("Month stored: " + dashboard_data['month']);
                console.log("Day stored: " + dashboard_data['day']);
            }
            
            else if (step === 3 && manButton && womanButton) {
                // 각 버튼의 상태를 직접 확인하여 성별 결정
                if (manButton.style.fontWeight === '900') {
                    dashboard_data['gender'] = 'male';
                } else if (womanButton.style.fontWeight === '900') {
                    dashboard_data['gender'] = 'female';
                }
                if (!dashboard_data['gender']) {
                    alert('성별을 선택해주세요.');
                    return [dashboard_data, step];
                }
                dashboard_data['FinalStep'] = true;
                console.log("Final Step stored: " + dashboard_data['FinalStep']);
                console.log("Gender stored: " + dashboard_data['gender']);
            }
            
            console.log("Updated dashboard_data :", dashboard_data);
            return [dashboard_data, step < MAX_STEP ? step + 1 : step];
        }
        """,
        [Output('dashboard-add-store', 'data'),
         Output('dashboard-add-current-step-store', 'data'), ],
        Input('dashboard-add-next-button', 'n_clicks'),
        [State('dashboard-add-current-step-store', 'data'),
         State('dashboard-add-store', 'data')],
    )

    @app.callback(
        [Output('dashboard-add-input-gender-man', 'style'),
         Output('dashboard-add-input-gender-woman', 'style')],
        [Input('dashboard-add-input-gender-man', 'n_clicks'),
         Input('dashboard-add-input-gender-woman', 'n_clicks')]
    )
    def update_button_style(man_clicks, woman_clicks):
        # 기본 스타일 설정
        default_style = {'font-weight': 'normal'}
        active_style = {'font-weight': '900'}

        # 클릭 컨텍스트를 확인하여 누가 클릭되었는지 확인
        ctx = callback_context
        if not ctx.triggered:
            return default_style, default_style
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        # 버튼 ID에 따라 스타일 변경
        if button_id == 'dashboard-add-input-gender-man':
            return active_style, default_style
        elif button_id == 'dashboard-add-input-gender-woman':
            return default_style, active_style
        else:
            return default_style, default_style

    @app.callback(
        [Output('dashboard-add-current-step-store', 'data', allow_duplicate=True),
         Output('dashboard-add', 'href')],
        [Input('dashboard-add-back-button', 'n_clicks')],
        [State('dashboard-add-current-step-store', 'data')],
        prevent_initial_call=True
    )
    def handle_back_button(n_clicks, current_step):
        if current_step == 1:
            return current_step, "/beha-pulse/main/dashboard/"  # 첫 페이지에서는 /beha-pulse/로 이동
        elif current_step == 5:
            return 1, "/beha-pulse/main/dashboard/"
        else:
            return current_step - 1, None  # 이전 단계로 이동

    # 현재 단계에 따라 signup-next-button의 텍스트를 동적으로 변경하는 콜백
    @app.callback(
        [Output('dashboard-add-next-button', 'children'),
         Output('dashboard-add-next-button', 'href')],
        [Input('dashboard-add-current-step-store', 'data')]
    )
    def update_next_button_text(current_step):
        if current_step == 4:
            return "홈화면으로 나가기", '/beha-pulse/main/dashboard/'
        else:
            return "다음", None

    @app.callback(
        [Output('dashboard-add-store', 'data', allow_duplicate=True),  # signup 데이터 업데이트
         Output('dashboard-add-current-step-store', 'data', allow_duplicate=True)],  # 단계 업데이트
        [Input('dashboard-add-next-button', 'n_clicks')],  # Next 버튼 클릭 감지
        [State('dashboard-add-store', 'data'),  # 현재 입력된 데이터
         State('dashboard-add-current-step-store', 'data')],  # 현재 단계
        prevent_initial_call=True
    )
    def register(n_clicks, data, step):
        if step == 3 and n_clicks and data['FinalStep']:
            required_fields = ['name', 'gender', 'year', 'month', 'day']
            if not all([data.get(key) for key in required_fields]):
                return data, 5  # 오류 단계로 설정

            birth = f"{data['year']}-{data['month']}-{data['day']}"
            gender = '남' if data['gender'] == 'male' else '여'

            payload = {
                'name': data['name'],
                'gender': gender,
                'birth': birth,
                'location': '',
            }
            api_url = f'http://{server["server"]["host"]}:{server["server"]["port"]}/dashboard/register'

            try:
                response = requests.post(api_url, json=payload)
                if response.status_code == 200:
                    personId = response.json()['personId']
                    person_api_url = f'http://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard/register'
                    person_payload = {
                        'personId': personId,
                        'userEmail': session.get('user_id')
                    }
                    person_response = requests.post(person_api_url, json=person_payload)
                    if person_response.status_code == 200:
                        return data, 4
                    else:
                        return data, 5
                else:
                    return data, 5
            except requests.exceptions.RequestException as e:
                return data, 5

        return no_update, no_update

    @app.callback(
        [Output('overlay-background', 'style', allow_duplicate=True),
         Output('delete-overlay-container', 'style', allow_duplicate=True),
         Output('delete-overlay-text', 'children', ),
         Output('delete-overlay-buttons', 'style')
         ],
        [Input('dashboard-delete-button-confirm', 'n_clicks'),
         Input('overlay-background', 'n_clicks'),
         Input({'type': 'checkbox', 'index': ALL}, 'value')
         ],
        [State('overlay-background', 'style'),
         State('delete-overlay-container', 'style')],
        prevent_initial_call=True
    )
    def toggle_overlay(n_clicks_button, n_clicks_background, selected_values, background_style, container_style):
        # 팝업을 켜는 경우
        ctx = callback_context
        if not ctx.triggered:
            return background_style, container_style
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        button_show = {'display': 'flex'}

        # 버튼 클릭으로 열기
        if triggered_id == 'dashboard-delete-button-confirm' and n_clicks_button:
            background_style['display'] = 'block'
            container_style['display'] = 'block'
        # 오버레이 클릭으로 닫기
        elif triggered_id == 'overlay-background' and n_clicks_background:
            background_style['display'] = 'none'
            container_style['display'] = 'none'

        # 선택된 personId 및 name 추출
        selected_persons = [value[0] for value in selected_values if value]  # 체크된 값에서 사전 데이터 추출

        # 선택된 이름 리스트
        selected_names = [person['name'] for person in selected_persons]

        # 선택된 사람 수에 따라 출력 텍스트 결정
        if len(selected_names) == 1:
            # text = f"{selected_names[0]} 님을 <br> 정말 삭제하시겠습니까?"
            text = [f"{selected_names[0]} 님을", html.Br(), "정말 삭제하시겠습니까?"]
        elif len(selected_names) > 1:
            text = [f"{selected_names[0]} 외 {len(selected_names) - 1}명을", html.Br(), "삭제하시겠습니까?"]
        else:
            text = "아무도 선택 되지 않았습니다."  # 선택된 사람이 없는 경우
            button_show = {'display': 'none'}

        return background_style, container_style, text, button_show

    @app.callback(
        Output('dashboard-delete', 'href'),
        Input('delete-confirm-button', 'n_clicks'),
        [State({'type': 'checkbox', 'index': ALL}, 'value')],
    )
    def delete_dashboard(n_clicks, selected_values):
        if n_clicks:
            selected_persons = [value[0] for value in selected_values if value]  # 체크된 값에서 사전 데이터 추출

            selected_names = [person['name'] for person in selected_persons]
            selected_ids = [person['personId'] for person in selected_persons]

            del_count = 0
            for idx in range(len(selected_persons)):

                api_url = f'http://{server["server"]["host"]}:{server["server"]["port"]}/dashboard/delete/{selected_ids[idx]}/{selected_names[idx]}'

                try:
                    response = requests.delete(api_url)
                    if response.status_code == 200:
                        del_count += 1
                    else:
                        return no_update

                except requests.exceptions.RequestException as e:
                    return no_update
            if del_count == len(selected_persons):
                return '/beha-pulse/main/dashboard/'
            else:
                return no_update
        return no_update

    @app.callback(
        [Output('overlay-background', 'style', allow_duplicate=True),
         Output('delete-overlay-container', 'style', allow_duplicate=True),
         Input('delete-cancel-button', 'n_clicks')],
        [State('overlay-background', 'style'),
         State('delete-overlay-container', 'style')],
        prevent_initial_call=True
    )
    def cancel_delete(n_clicks, background_style, container_style):
        if n_clicks:
            background_style['display'] = 'none'
            container_style['display'] = 'none'
        return background_style, container_style
