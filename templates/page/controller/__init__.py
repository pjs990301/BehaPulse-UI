
def set_controller(app):
    from .login import login_controller
    from .signup import signup_controller
    from .password import password_controller
    # from .home import
    from .device import device_controller
    from .sidebar import sidebar_controller, toggler_controller
    from .dashboard import dashboard_controller

    login_controller(app)
    signup_controller(app)
    password_controller(app)
    toggler_controller(app)
    device_controller(app)
    sidebar_controller(app)
    dashboard_controller(app)



