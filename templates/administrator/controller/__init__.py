
def set_controller(app):
    from .login import login_controller
    from .signup import signup_controller
    from .password import password_controller
    # from .main_page import main_controller

    login_controller(app)
    signup_controller(app)
    password_controller(app)
    # main_controller(app)