from .login import *
from .signup import *

url_to_layout = {
    '/admin': login_layout,
    '/admin/signup': signup_layout,
}


def set_layout(app):
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        return url_to_layout.get(pathname, login_layout)()
