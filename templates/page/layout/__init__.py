from .signup import *
from .splash import *
from .login import *
from .main import *
from .content import *
from .find_id import *
from .find_pw import *

from dash.dependencies import Input, Output, State

url_to_layout = {
    '/beha-pulse/': splash_layout,
    '/beha-pulse/signup/': signup_layout,
    '/beha-pulse/login/': login_layout,
    '/beha-pulse/main/': main_layout,
    '/beha-pulse/find-id/': find_id_layout,
    '/beha-pulse/find-password/': find_pw_layout,
}

main_to_device_layout = {
    '/beha-pulse/main/device/add/': device_add_layout,
    '/beha-pulse/main/device/edit/': device_edit_layout,
    '/beha-pulse/main/device/detail/': device_detail_layout,
}

main_to_sub = {
    '/beha-pulse/main/': main_content,
    '/beha-pulse/main/device/': device_content,
    '/beha-pulse/main/dashboard/': dashboard_content,
    '/beha-pulse/main/user/': user_content,
}

not_need_login_layout = [
    '/beha-pulse/',
    '/beha-pulse/signup/',
    '/beha-pulse/login/',
    '/beha-pulse/find-id/',
    '/beha-pulse/find-password/',
]


def set_layout(app):
    @app.callback(
        [Output('page', 'children'),
         Output('redirect', 'href')],
        [Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def display_page(pathname):
        layout = html.Div()
        redirect_url = None

        if not session.get('login'):  # 로그인이 되어 있지 않은 경우
            if pathname in not_need_login_layout:  # 로그인 없이 이용할 수 있는 경우
                layout = url_to_layout.get(pathname, splash_layout)()

            else:  # 반드시 로그인이 필요한 레이아웃의 경우,
                redirect_url = '/beha-pulse/login/'

        else:  # 로그인 되어 있는 경우
            # 로그인이 되어있는 데 로그인이 필요없는 레이아웃을 요청하는 경우
            if pathname in not_need_login_layout:
                redirect_url = '/beha-pulse/main/'

            else:  # 로그인이 되어 있는 데 로그인이 필요한 레이아웃을 요청한 경우
                if pathname == '/beha-pulse/main/':
                    layout = main_layout()

                elif pathname in main_to_device_layout:
                    layout = main_to_device_layout.get(pathname, main_layout)()

                # URL이 이상한 경우
                elif pathname.startswith('/beha-pulse/') and pathname != '/beha-pulse/main/':
                    redirect_url = '/beha-pulse/main/'
                else:  # 로그인이 되어있는 데, 정해지지 않은 URL로 요청한 경우
                    redirect_url = '/beha-pulse/main/'

            # # 로그인이 되어있고 로그인이 필요 있는 레이아웃을 요청하는 경우
            # else:
            #     if pathname == '/beha-pulse/main/':
            #         layout = main_layout()
            #
            #     elif pathname.startswith('/beha-pulse/main/') and pathname != '/beha-pulse/main/':
            #         redirect_url = '/beha-pulse/main/'
            #
            #     elif pathname in main_to_device_layout:
            #         layout = main_to_device_layout.get(pathname, main_layout)()
            #
            #     else:
            #         layout = url_to_layout.get(pathname, main_layout)()

        return layout, redirect_url


def set_main_content(app):
    @app.callback(
        Output('main-content', 'children'),
        [Input('main-url', 'pathname')]
    )
    def display_main_content(pathname):
        # URL 경로에 따라 콘텐츠를 결정
        content_function = main_to_sub.get(pathname)
        if content_function:
            return content_function()
        else:
            return main_content()  # 기본적으로 main_content 반환
