"""
    The app's main page. We control routes in here.
"""

from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from app import server

from flask_login import logout_user, current_user
from models.user import UserModel
from views.core import admin_users, admin_roles, admin_groups, login, error, profile
from views.page import (
    overview,
)

# using for decoding the URL. for example detail pages
import urllib.parse as parser

content = html.Div(id="pageContent")

sidebar = html.Div(id="sidebarDiv")

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div([sidebar, content]),
    ]
)

################################################################################
# HANDLE PAGE ROUTING - IF USER NOT LOGGED IN, ALWAYS RETURN TO LOGIN SCREEN
################################################################################


@app.callback(Output("pageContent", "children"), [Input("url", "pathname")])
def displayPage(pathname):
    ###########################################
    ############### CORE Routes ###############
    ###########################################
    if pathname == "/":
        if current_user.is_authenticated:
            return overview.get_layout(current_user)
        else:
            return login.layout

    elif pathname.startswith("/admin/users/"):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return admin_users.get_layout(current_user)
            else:
                return error.layout
        else:
            return login.layout

    elif pathname.startswith("/admin/roles/"):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return admin_roles.get_layout(current_user)
            else:
                return error.layout
        else:
            return login.layout

    elif pathname.startswith("/admin/groups/"):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return admin_groups.get_layout(current_user)
            else:
                return error.layout
        else:
            return login.layout

    elif pathname == "/profile/":
        if current_user.is_authenticated:
            return profile.get_layout(current_user)
        else:
            return login.layout

    elif pathname == "/logout/":
        if current_user.is_authenticated:
            logout_user()
            return login.layout
        else:
            return login.layout

    ###########################################
    ############### Page Routes ###############
    ###########################################

    elif pathname == "/overview/":
        if current_user.is_authenticated:
            return overview.get_layout(current_user)
        else:
            return login.layout
    else:
        return error.layout


################################################################################
# ONLY SHOW NAVIGATION BAR WHEN A USER IS LOGGED IN
################################################################################
@app.callback(Output("sidebarDiv", "children"), [Input("pageContent", "children")])
def navBar(input1):
    if current_user.is_authenticated:
        navBarContents = [
            dbc.NavItem(dbc.NavLink("Overview", href="/overview/"))
            if current_user.is_my_role("page-overview")
            else "",
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="User",
                children=[
                    dbc.DropdownMenuItem("Profile", href="/profile/"),
                    dbc.DropdownMenuItem("Admin Users", href="/admin/users/")
                    if current_user.is_admin
                    else "",
                    dbc.DropdownMenuItem("Admin Roles", href="/admin/roles/")
                    if current_user.is_admin
                    else "",
                    dbc.DropdownMenuItem("Admin Groups", href="/admin/groups/")
                    if current_user.is_admin
                    else "",
                    dbc.DropdownMenuItem("Logout", href="/logout/"),
                ],
            ),
        ]
        navbar = dbc.Nav(
            id="navBar",
            children=navBarContents,
            vertical=True,
            pills=True,
        )
        return html.Div(
            [
                dcc.Store(id="navbar-status-store", data="OPEN"),
                html.Img(
                    src="/assets/navbar-icon.png",
                    id="navbar-open-btn",
                    n_clicks=0,
                ),
                html.Div(
                    [
                        html.Div(
                            children=[
                                html.Img(
                                    src="/assets/logo-white.png",
                                    className="img-fluid",
                                    width=180,
                                ),
                                html.Img(
                                    src="/assets/icon-back.png",
                                    width=25,
                                    height=25,
                                    style={"margin-left": "15px"},
                                    id="navbar-close-btn",
                                    n_clicks=0,
                                ),
                            ],
                            style={"display": "inline-block"},
                        ),
                        html.Hr(),
                        navbar,
                    ],
                    id="navbarDiv",
                    className="navbarDiv",
                ),
            ]
        )
    else:
        return ""


@app.callback(
    [Output("navbarDiv", "className"), Output("navbar-status-store", "data")],
    [
        Input("navbar-open-btn", "n_clicks"),
        Input("navbar-close-btn", "n_clicks"),
    ],
    State("navbar-status-store", "data"),
)
def open_close_sidebar(open_n_clicks, close_n_clicks, data):
    if open_n_clicks >= 1:
        if data == "CLOSE":
            open_n_clicks = 0
            return ("navbarDivOpen", "OPEN")
        elif data == "OPEN":
            open_n_clicks = 0
            return ("navbarDiv", "CLOSE")
    else:
        open_n_clicks = 0
        return ("navbarDiv", "CLOSE")
    if close_n_clicks >= 1:
        if data == "CLOSE":
            close_n_clicks = 0
            return ("navbarDivOpen", "OPEN")
        elif data == "OPEN":
            close_n_clicks = 0
            return ("navbarDiv", "CLOSE")
    else:
        close_n_clicks = 0
        return ("navbarDiv", "CLOSE")


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
