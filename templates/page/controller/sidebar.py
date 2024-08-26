from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
from datetime import datetime


def sidebar_controller(app):
    @app.callback(
        Output('redirect', 'href'),
        Output('sidebar', 'style'),
        Input('logout-button', 'n_clicks')
    )
    def logout(n_clicks):
        if n_clicks:
            session.pop('logged_in', None)
            session.pop('user_email', None)
            session.pop('user_name', None)

            # 사이드바 닫기
            sidebar_style = {"transform": "translateY(-120%)"}

            return '/admin/', sidebar_style

        return no_update, no_update

    @app.callback(
        Output('sidebar-userName', 'children'),
        Input('url', 'pathname'))  # 페이지가 로드될 때마다 콜백 실행
    def update_user_name(pathname):
        user_name = session.get('user_name', '홍길동')
        return f'{user_name}님'


def toggler_controller(app):
    app.clientside_callback(
        """
        function(n_clicks_toggle, n_clicks_overlay, n_clicks_navlink) {
            var button = document.getElementById('navbar-toggler');
            var sidebar = document.getElementById('sidebar');
            var overlay = document.getElementById('overlay');
            var sidebar_content = document.getElementById('sidebar-content');
            var sidebar_footer = document.getElementById('sidebar-footer');

            if (!button || !sidebar || !overlay || !sidebar_content) {
                console.error("Button, sidebar, overlay, or sidebar_content element not found.");
                return;
            }

            // Ensure data-open is defined with a default value
            if (sidebar.getAttribute('data-open') === null || sidebar.getAttribute('data-open') === undefined) {
                sidebar.setAttribute('data-open', 'false');
            }

            // Sidebar toggle button clicked
            if (n_clicks_toggle && sidebar.getAttribute('data-open') === 'false') {
                // Open sidebar
                var rect = button.getBoundingClientRect();
                sidebar.style.top = (rect.top) + 'px';  // Position below the button
                sidebar.style.left = rect.left + 'px';  // Align left edge with the button
                sidebar.style.transform = 'translateY(0px)';
                overlay.style.display = 'block';
                sidebar.setAttribute('data-open', 'true');

                sidebar_content.style.top = (rect.bottom) + 'px'; 

                var sidebar_rect = sidebar.getBoundingClientRect();                
                sidebar_content.style.height = sidebar_rect.height - rect.height + 'px';

                var sidebar_content_rect = sidebar_content.getBoundingClientRect();

                var sidebar_footer_rect = sidebar_footer.getBoundingClientRect();

                // Reset overlay clicks count to prevent immediate closure
                overlay.setAttribute('data-clicked', 'false');
                return;
            }

            // Overlay clicked or NavLink clicked
            if ((n_clicks_overlay || n_clicks_navlink) && sidebar.getAttribute('data-open') === 'true') {
                // Close sidebar
                sidebar.style.transform = 'translateY(-120%)';
                overlay.style.display = 'none';
                sidebar.setAttribute('data-open', 'false');

                // Mark overlay as clicked to prevent reopening
                if (n_clicks_overlay) {
                    overlay.setAttribute('data-clicked', 'true');
                }
                return;
            }
        }
        """,
        Output('dummy-div', 'children'),
        [Input('navbar-toggler', 'n_clicks'), Input('overlay', 'n_clicks'), Input('sidebar', 'n_clicks')]
    )

    # 현재 시간 업데이트 콜백
    @app.callback(
        Output('date-time', 'children'),
        Input('interval-component', 'n_intervals')
    )
    def update_time(n):
        now = datetime.now()
        date_str = now.strftime("%Y년 %m월 %d일")
        time_str = now.strftime("%H시 %M분")
        return [date_str, html.Br(), time_str]
