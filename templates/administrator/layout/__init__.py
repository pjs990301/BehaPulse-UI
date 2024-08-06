from .login import *
from .signup import *
from .password import *
from .main_page import *

from .content import *

url_to_layout = {
    '/admin/': login_layout,
    '/admin/signup': signup_layout,
    '/admin/password': find_password_layout,
    '/admin/main': main_layout
}
url_to_content = {
    '/admin/home': home_layout,
    '/admin/dashboard': dashbord_layout,
    '/admin/projects': project_layout,
}


def set_layout(app):
    @app.callback(Output('page', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname in url_to_layout.keys():
            return url_to_layout.get(pathname)()
        return main_layout()


def set_content(app):
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_content(pathname):
        content_function = url_to_content.get(pathname)
        if content_function:
            return content_function()
        else:
            return home_layout()