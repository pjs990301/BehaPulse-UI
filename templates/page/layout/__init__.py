from .login import *
from .signup import *
from .password import *
from .main_page import *

from .content import *

from .smartthings import smartthings_layout
from .smartthings_device import smartthings_device_layout

from dash import no_update, callback_context, State

url_to_layout = {
    '/': login_layout,
    '/admin/': login_layout,
    '/admin/signup': signup_layout,
    '/admin/password': find_password_layout,
    '/admin/main': main_layout,
    '/admin/smartthings': smartthings_layout,
    '/admin/smartthings_device': smartthings_device_layout,
}

url_to_content = {
    '/admin/home': home_layout,
    '/admin/dashboard': dashbord_layout,
    '/admin/device': device_layout,
    '/admin/device/detail': device_detail_layoout,
    '/admin/device/edit': device_edit_layout,
    '/admin/device/add': device_add_layout,
    '/admin/dashboard/add': dashboard_add_layout,
    '/admin/dashboard/detail': dashboard_detail_layout,
    '/admin/dashboard/detail/info': dashboard_person_info_layout,
    '/admin/dashboard/detail/edit': dashboard_person_edit_layout,
    # '/admin/smartthings': smartthings_layout,
    '/admin/smartthings': smartthings_layout,
    '/admin/smartthings_device': smartthings_device_layout,
}


def set_layout(app):
    @app.callback(
        Output('page', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        # 로그인이 필요한 페이지인지 확인
        if not session.get('logged_in'):
            # 로그인 없이 접근 가능한 페이지들에 대한 예외 처리
            if pathname in ['/admin/signup', '/admin/password', '/admin/']:
                return url_to_layout.get(pathname, login_layout)()

            # 그 외의 모든 페이지는 로그인 페이지로 리디렉션
            return dcc.Location(pathname='/admin/', id='redirect')

        # 로그인된 상태에서 로그인 페이지로 접근 시 메인 페이지로 리디렉션
        if session.get('logged_in') and pathname == '/admin/':
            return dcc.Location(pathname='/admin/main', id='redirect')

        # 각 페이지에 맞는 레이아웃 반환
        if pathname in url_to_layout.keys():
            return url_to_layout.get(pathname)()
        return main_layout()


def set_content(app):
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_content(pathname):
        # 로그인 여부 확인
        if not session.get('logged_in'):
            # 로그인 없이 접근 가능한 페이지들에 대한 예외 처리
            if pathname in ['/admin/signup', '/admin/password', '/admin/']:
                return no_update

            # 그 외의 모든 페이지는 로그인 페이지로 리디렉션
            return dcc.Location(pathname='/admin/', id='redirect')

        # 각 pathname에 해당하는 content 레이아웃 반환
        content_function = url_to_content.get(pathname)
        if content_function:
            return content_function()
        else:
            return home_layout()
