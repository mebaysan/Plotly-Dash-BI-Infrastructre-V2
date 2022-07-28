from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app
from models.user import UserModel
from flask_login import login_user
from werkzeug.security import check_password_hash


username_input = html.Div(
    id="form-body",
    children=[
        dbc.Label("Email Address", html_for="example-email"),
        dbc.Input(
            type="email",
            id="emailBox",
            placeholder="Enter Email",
            n_submit=0,
            value="admin@admin.com",
        ),
    ],
)

password_input = html.Div(
    id="form-body",
    children=[
        dbc.Label("Password", html_for="example-password"),
        dbc.Input(
            type="password",
            id="passwordBox",
            placeholder="Enter password",
            n_submit=0,
            value="123",
        ),
    ],
)

submit_button = dbc.Button(
    children="Login", n_clicks=0, type="submit", id="loginButton", className="dark-blue"
)

form = html.Div(
    id="auth-inputs",
    children=[
        username_input,
        password_input,
        html.Div(
            className="auth-forgot",
            children=[
                dbc.FormText(html.A("Need help? Contact us", href="/")),
            ],
        ),
    ],
)

layout = dbc.Container(
    id="authentication",
    children=[
        dcc.Location(id="urlLogin", refresh=True),
        dbc.Row(
            children=[
                html.Div(
                    className="col-lg-6",
                    id="left-area",
                    children=[html.Img(src="/assets/auth-left.png")],
                ),
                html.Div(
                    className="col-lg-6",
                    id="right-area",
                    children=[
                        html.Div(
                            id="authentication-container",
                            children=[
                                html.Div(
                                    id="auth-logo",
                                    children=[html.Img(src="/assets/logo-black.png")],
                                ),
                                html.Div(
                                    id="auth-header",
                                    children=[
                                        html.H1("Welcome to"),
                                        html.H2("Management Dashboard"),
                                    ],
                                ),
                                html.Div(id="auth-action", children=[form]),
                                html.Div(id="auth-button", children=[submit_button]),
                            ],
                        )
                    ],
                ),
            ],
        ),
    ],
)


################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - REDIRECT TO PAGE1 IF LOGIN DETAILS ARE CORRECT
################################################################################
@app.callback(
    Output("urlLogin", "pathname"),
    [
        Input("loginButton", "n_clicks"),
        Input("emailBox", "n_submit"),
        Input("passwordBox", "n_submit"),
    ],
    [State("emailBox", "value"), State("passwordBox", "value")],
)
def sucess(n_clicks, emailSubmit, passwordSubmit, email, password):
    user = UserModel.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return "/"
        else:
            pass
    else:
        pass


################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF LOGIN DETAILS INCORRECT (USERNAME)
################################################################################
@app.callback(
    Output("emailBox", "className"),
    [
        Input("loginButton", "n_clicks"),
        Input("emailBox", "n_submit"),
        Input("passwordBox", "n_submit"),
    ],
    [State("emailBox", "value"), State("passwordBox", "value")],
)
def update_output_username(n_clicks, emailSubmit, passwordSubmit, email, password):
    if (n_clicks > 0) or (emailSubmit > 0) or (passwordSubmit > 0):
        user = UserModel.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return "form-control"
            else:
                return "form-control is-invalid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"


################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF LOGIN DETAILS INCORRECT (PASSWORD)
################################################################################
@app.callback(
    Output("passwordBox", "className"),
    [
        Input("loginButton", "n_clicks"),
        Input("emailBox", "n_submit"),
        Input("passwordBox", "n_submit"),
    ],
    [State("emailBox", "value"), State("passwordBox", "value")],
)
def update_output_password(n_clicks, emailSubmit, passwordSubmit, email, password):
    if (n_clicks > 0) or (emailSubmit > 0) or (passwordSubmit > 0):
        user = UserModel.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return "form-control"
            else:
                return "form-control is-invalid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"
