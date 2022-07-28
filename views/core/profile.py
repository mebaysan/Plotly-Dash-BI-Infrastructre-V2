from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app
from flask_login import current_user

from werkzeug.security import check_password_hash


def get_layout(user):
    layout = dbc.Container(
        [
            html.Br(),
            html.Div(
                [
                    dcc.Location(id="urlProfile", refresh=True),
                    html.H3("Profile Management"),
                    html.Hr(),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label("Name:"),
                                    html.Br(),
                                    html.Label("Email:"),
                                    html.Br(),
                                    html.Label("Position:"),
                                    html.Br(),
                                    html.Label("Group:"),
                                    html.Br(),
                                    html.Label("Holding:"),
                                    html.Br(),
                                    html.Label("Company:"),
                                    html.Br(),
                                ],
                                className="col-2",
                            ),
                            html.Div(
                                [
                                    html.Label(
                                        id="profile-name", className="text-success"
                                    ),
                                    html.Br(),
                                    html.Label(
                                        id="profile-email", className="text-success"
                                    ),
                                    html.Br(),
                                    html.Label(
                                        id="profile-position", className="text-success"
                                    ),
                                    html.Br(),
                                    html.Label(
                                        id="profile-group", className="text-success"
                                    ),
                                    html.Br(),
                                    html.Label(
                                        id="profile-holding", className="text-success"
                                    ),
                                    html.Br(),
                                    html.Label(
                                        id="profile-company", className="text-success"
                                    ),
                                    html.Br(),
                                ],
                                className="col-2",
                            ),
                            html.Div(
                                [
                                    html.Label("Old Password: "),
                                    dcc.Input(
                                        id="oldPassword",
                                        type="password",
                                        className="form-control",
                                        placeholder="Old password",
                                        n_submit=0,
                                        style={"width": "40%"},
                                    ),
                                    html.Br(),
                                    html.Label("New Password: "),
                                    dcc.Input(
                                        id="newPassword1",
                                        type="password",
                                        className="form-control",
                                        placeholder="New password",
                                        n_submit=0,
                                        style={"width": "40%"},
                                    ),
                                    html.Br(),
                                    html.Label("Retype New Password: "),
                                    dcc.Input(
                                        id="newPassword2",
                                        type="password",
                                        className="form-control",
                                        placeholder="Retype new password",
                                        n_submit=0,
                                        style={"width": "40%"},
                                    ),
                                    html.Br(),
                                    html.Button(
                                        children="Update Password",
                                        id="updatePasswordButton",
                                        n_clicks=0,
                                        type="submit",
                                        className="baysansoft-btn-active",
                                        style={"width": "170px"},
                                    ),
                                    html.Br(),
                                    html.Div(id="updateSuccess"),
                                ],
                                className="col-8",
                            ),
                        ],
                        className="row",
                    ),
                ],
                className="jumbotron",
            ),
        ]
    )
    return layout


@app.callback(
    [
        Output("profile-name", "children"),
        Output("profile-email", "children"),
        Output("profile-position", "children"),
        Output("profile-group", "children"),
        Output("profile-holding", "children"),
        Output("profile-company", "children"),
    ],
    Input("pageContent", "children"),
)
def current_user_info(pageContent):
    try:
        return (
            current_user.name,
            current_user.email,
            current_user.position,
            current_user.group,
            current_user.holding,
            current_user.company,
        )
    except AttributeError:
        return ("", "", "", "", "", "")


################################################################################
# UPDATE PWD BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF OLD PWD IS NOT CURR PWD
################################################################################
@app.callback(
    Output("oldPassword", "className"),
    [
        Input("updatePasswordButton", "n_clicks"),
        Input("newPassword1", "n_submit"),
        Input("newPassword2", "n_submit"),
    ],
    [
        State("pageContent", "children"),
        State("oldPassword", "value"),
        State("newPassword1", "value"),
        State("newPassword2", "value"),
    ],
)
def validateOldPassword(
    n_clicks,
    newPassword1Submit,
    newPassword2Submit,
    pageContent,
    oldPassword,
    newPassword1,
    newPassword2,
):
    if (n_clicks > 0) or (newPassword1Submit > 0) or (newPassword2Submit) > 0:
        if check_password_hash(current_user.password, oldPassword):
            return "form-control is-valid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"


# ###############################################################################
# UPDATE PWD BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF NEW PASSWORDS ARE NOT THE SAME
# ###############################################################################
@app.callback(
    Output("newPassword1", "className"),
    [
        Input("updatePasswordButton", "n_clicks"),
        Input("newPassword1", "n_submit"),
        Input("newPassword2", "n_submit"),
    ],
    [State("newPassword1", "value"), State("newPassword2", "value")],
)
def validatePassword1(
    n_clicks, newPassword1Submit, newPassword2Submit, newPassword1, newPassword2
):
    if (n_clicks > 0) or (newPassword1Submit > 0) or (newPassword2Submit) > 0:
        if newPassword1 == newPassword2:
            return "form-control is-valid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"


# ###############################################################################
# UPDATE PWD BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF NEW PASSWORDS ARE NOT THE SAME
# ###############################################################################
@app.callback(
    Output("newPassword2", "className"),
    [
        Input("updatePasswordButton", "n_clicks"),
        Input("newPassword1", "n_submit"),
        Input("newPassword2", "n_submit"),
    ],
    [State("newPassword1", "value"), State("newPassword2", "value")],
)
def validatePassword2(
    n_clicks, newPassword1Submit, newPassword2Submit, newPassword1, newPassword2
):
    if (n_clicks > 0) or (newPassword1Submit > 0) or (newPassword2Submit) > 0:
        if newPassword1 == newPassword2:
            return "form-control is-valid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"


################################################################################
# UPDATE PWD BUTTON CLICKED / ENTER PRESSED - UPDATE DATABASE WITH NEW PASSWORD
################################################################################
@app.callback(
    Output("updateSuccess", "children"),
    [
        Input("updatePasswordButton", "n_clicks"),
        Input("newPassword1", "n_submit"),
        Input("newPassword2", "n_submit"),
    ],
    [
        State("pageContent", "children"),
        State("oldPassword", "value"),
        State("newPassword1", "value"),
        State("newPassword2", "value"),
    ],
)
def changePassword(
    n_clicks,
    newPassword1Submit,
    newPassword2Submit,
    pageContent,
    oldPassword,
    newPassword1,
    newPassword2,
):
    if (n_clicks > 0) or (newPassword1Submit > 0) or (newPassword2Submit) > 0:
        if (
            check_password_hash(current_user.password, oldPassword)
            and newPassword1 == newPassword2
        ):
            try:
                current_user.set_password(newPassword1)
                current_user.save_to_db()
                return html.Div(
                    children=["Update Successful"], className="text-success"
                )
            except Exception as e:
                return html.Div(
                    children=["Update Not Successful: {e}".format(e=e)],
                    className="text-danger",
                )
        else:
            return html.Div(children=["Old Password Invalid"], className="text-danger")
