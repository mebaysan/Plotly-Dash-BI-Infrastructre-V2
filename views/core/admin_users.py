from dash import dcc, html, dash_table as dt
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State, ALL, MATCH

from app import app
from models.user import AuthorizationGroupModel, UserModel, RoleModel

from components.core.page import header
from components.users.table import get_users_table

from utilities.password import generate_password


import time


def get_layout(user):
    ROW_MARGIN_TOP = "50px"
    layout = dbc.Container(
        [
            header("User & Access Management", "Management Dashboard"),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Input(
                                placeholder="Search in users...",
                                style={"width": "280px", "height": "40px"},
                                id="search-in-users-text",
                                n_submit=0,
                            ),
                            html.Button(
                                "Search",
                                className="baysansoft-btn-active",
                                style={"width": "75px", "margin-left": "15px"},
                                id="search-in-users-btn",
                                n_clicks=0,
                            ),
                            html.Button(
                                "Add User Access",
                                className="baysansoft-btn-active",
                                style={"width": "160px", "float": "right"},
                                id="users-admin-add-modal-open-btn",
                                n_clicks=0,
                            ),
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(
                                        dbc.ModalTitle(
                                            [
                                                html.Div(
                                                    [
                                                        html.H5(
                                                            html.B("Create an Account")
                                                        ),
                                                        html.H6("Management Dashboard"),
                                                    ],
                                                    className="core-page-header-div",
                                                )
                                            ]
                                        )
                                    ),
                                    dbc.ModalBody(
                                        [
                                            dbc.Row(
                                                [
                                                    html.Div(
                                                        [
                                                            dbc.Label("Name Surname "),
                                                            dcc.Input(
                                                                id="new_user_name",
                                                                className="form-control",
                                                                n_submit=0,
                                                                style={"width": "90%"},
                                                            ),
                                                            html.Br(),
                                                            dbc.Label("Email Address"),
                                                            dcc.Input(
                                                                id="new_user_email",
                                                                type="email",
                                                                className="form-control",
                                                                n_submit=0,
                                                                style={"width": "90%"},
                                                            ),
                                                            html.Br(),
                                                            dbc.Label("Position "),
                                                            dcc.Input(
                                                                id="new_user_position",
                                                                className="form-control",
                                                                n_submit=0,
                                                                style={"width": "90%"},
                                                            ),
                                                            html.Br(),
                                                            dbc.Label("Admin "),
                                                            dcc.Dropdown(
                                                                id="is_new_user_admin",
                                                                style={"width": "90%"},
                                                                options=[
                                                                    {
                                                                        "label": "Yes",
                                                                        "value": 1,
                                                                    },
                                                                    {
                                                                        "label": "No",
                                                                        "value": 0,
                                                                    },
                                                                ],
                                                                value=0,
                                                                clearable=False,
                                                            ),
                                                            html.Br(),
                                                            html.P(
                                                                "When you created a user, system will send an auto generated password for the registered user email.",
                                                                style={
                                                                    "font-weight": "bold"
                                                                },
                                                            ),
                                                        ],
                                                        className="col-6",
                                                    ),
                                                    html.Div(
                                                        [
                                                            dbc.Label("Holding "),
                                                            dcc.Input(
                                                                id="new_user_holding",
                                                                className="form-control",
                                                                n_submit=0,
                                                                style={"width": "90%"},
                                                            ),
                                                            html.Br(),
                                                            dbc.Label("Group "),
                                                            dcc.Input(
                                                                id="new_user_group",
                                                                className="form-control",
                                                                n_submit=0,
                                                                style={"width": "90%"},
                                                            ),
                                                            html.Br(),
                                                            dbc.Label("Company "),
                                                            dcc.Input(
                                                                id="new_user_company",
                                                                className="form-control",
                                                                n_submit=0,
                                                                style={"width": "90%"},
                                                            ),
                                                            html.Br(),
                                                            dbc.Label("Groups "),
                                                            dcc.Dropdown(
                                                                options=[
                                                                    {
                                                                        "label": auth_group.name,
                                                                        "value": auth_group.id,
                                                                    }
                                                                    for auth_group in AuthorizationGroupModel.get_all()
                                                                ],
                                                                multi=True,
                                                                id="new_user_auth_groups",
                                                            ),
                                                            html.Br(),
                                                            dbc.Button(
                                                                children="Create User",
                                                                id="create_new_user_btn",
                                                                n_clicks=0,
                                                                type="submit",
                                                                className="baysansoft-btn-active",
                                                            ),
                                                        ],
                                                        className="col-6",
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                ],
                                id="users-admin-add-modal-open-modal",
                                size="lg",
                                is_open=False,
                            ),
                        ],
                        className="col",
                    )
                ],
                style={"margin-top": ROW_MARGIN_TOP},
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(id="admin_users_users_table-div"),
                        ],
                        className="col",
                    ),
                ],
                className="row",
                style={"margin-top": ROW_MARGIN_TOP},
            ),
        ]
    )
    return layout


################################################################################
# OPEN USER ADD MODAL
################################################################################
@app.callback(
    Output("users-admin-add-modal-open-modal", "is_open"),
    [
        Input("users-admin-add-modal-open-btn", "n_clicks"),
        Input("create_new_user_btn", "n_clicks"),
    ],
)
def toggle_modal(n1, n2):
    if n1 > 0 or n2 > 0:
        return True
    return False


################################################################################
# CREATE USER BUTTON CLICKED - UPDATE DATABASE WITH NEW USER
################################################################################
@app.callback(
    [
        Output("admin_users_users_table-div", "children"),
        Output("create_new_user_btn", "n_clicks"),
        Output("search-in-users-btn", "n_clicks"),
        Output("search-in-users-text", "n_submit"),
        Output("users-admin-add-modal-open-btn", "n_clicks"),
        # Clear form
        Output("search-in-users-text", "value"),
        Output("new_user_name", "value"),
        Output("new_user_email", "value"),
        Output("new_user_position", "value"),
        Output("is_new_user_admin", "value"),
        Output("new_user_holding", "value"),
        Output("new_user_group", "value"),
        Output("new_user_company", "value"),
        Output("new_user_auth_groups", "value"),
    ],
    [
        Input("create_new_user_btn", "n_clicks"),
        # to search in users
        Input("search-in-users-btn", "n_clicks"),
        Input("search-in-users-text", "n_submit"),
        # to delete user
        Input({"type": "users-table-delete-icon", "index": ALL}, "n_clicks"),
        # to refresh the table after updating a user
        Input({"type": "update_user_will_be_updated_btn", "index": ALL}, "n_clicks"),
    ],
    [
        State({"type": "users-table-delete-icon", "index": ALL}, "value"),
        State("search-in-users-text", "value"),
        State("new_user_name", "value"),
        State("new_user_email", "value"),
        State("new_user_position", "value"),
        State("is_new_user_admin", "value"),
        State("new_user_holding", "value"),
        State("new_user_group", "value"),
        State("new_user_company", "value"),
        State("new_user_auth_groups", "value"),
    ],
)
def create_user_modal_refresh_users_table(
    n_clicks,
    n_clicks2,
    n_submit,
    delete_icon_n_clicks,
    update_user_modal_btn_n_clicks,
    delete_icon_values,
    search_in_users_text,
    new_user_name,
    new_user_email,
    new_user_position,
    is_new_user_admin,
    new_user_holding,
    new_user_group,
    new_user_company,
    new_user_auth_groups,
):
    if n_clicks > 0:
        # create a new user
        try:
            new_password = generate_password(8)
            new_user = UserModel(
                new_user_name,
                new_user_position,
                new_user_holding,
                new_user_group,
                new_user_company,
                new_user_email,
                is_new_user_admin,
            )
            new_user.set_password(new_password)
            new_user.save_to_db()

            for auth_group_id in new_user_auth_groups:
                new_user.authorization_groups.append(
                    AuthorizationGroupModel.find_by_id(auth_group_id)
                )
            new_user.save_to_db()

            UserModel.send_user_password(new_user.id, new_password)
            return (
                get_users_table(UserModel.get_all()),
                0,
                0,
                0,
                0,
                "",
                "",
                "",
                "",
                0,
                "",
                "",
                "",
                [],
            )
        except Exception as e:
            return (
                get_users_table(UserModel.get_all()),
                0,
                0,
                0,
                0,
                "",
                "",
                "",
                "",
                0,
                "",
                "",
                "",
                [],
            )

    if n_clicks2 > 0 or n_submit > 0:
        # search in users
        return (
            get_users_table(
                UserModel.query.filter(
                    UserModel.email.contains(search_in_users_text)
                ).all()
            ),
            0,
            0,
            0,
            0,
            "",
            "",
            "",
            "",
            0,
            "",
            "",
            "",
            [],
        )

    if 1 in update_user_modal_btn_n_clicks and update_user_modal_btn_n_clicks != []:
        time.sleep(0.1)  # asenkron probleminden dolayı burada sleep yaptık
        return (
            get_users_table(UserModel.get_all()),
            0,
            0,
            0,
            0,
            "",
            "",
            "",
            "",
            0,
            "",
            "",
            "",
            [],
        )

    if len(delete_icon_n_clicks) > 0:
        if 1 in delete_icon_n_clicks:
            index = delete_icon_n_clicks.index(1)
            email = delete_icon_values[index]
            UserModel.find_by_email(email).delete_from_db()
            return (
                get_users_table(UserModel.get_all()),
                0,
                0,
                0,
                0,
                "",
                "",
                "",
                "",
                0,
                "",
                "",
                "",
                [],
            )

    return (
        get_users_table(UserModel.get_all()),
        0,
        0,
        0,
        0,
        "",
        "",
        "",
        "",
        0,
        "",
        "",
        "",
        [],
    )


################################################################################
# OPEN USER UPDATE MODAL & LOAD USER INFO TO FORM
################################################################################
@app.callback(
    Output({"type": "users-admin-update-modal", "index": MATCH}, "is_open"),
    Output({"type": "user_will_be_updated_name", "index": MATCH}, "value"),
    Output({"type": "user_will_be_updated_email", "index": MATCH}, "value"),
    Output({"type": "user_will_be_updated_position", "index": MATCH}, "value"),
    Output({"type": "is_user_will_be_updated_admin", "index": MATCH}, "value"),
    Output({"type": "user_will_be_updated_holding", "index": MATCH}, "value"),
    Output({"type": "user_will_be_updated_group", "index": MATCH}, "value"),
    Output({"type": "user_will_be_updated_company", "index": MATCH}, "value"),
    Output(
        {
            "type": "update_user_will_be_updated_authorization_groups_dropdown",
            "index": MATCH,
        },
        "value",
    ),
    [
        Input({"type": "users-table-update-icon", "index": MATCH}, "n_clicks"),
    ],
    [
        State({"type": "users-table-update-icon", "index": MATCH}, "value"),
        State({"type": "users-admin-update-modal", "index": MATCH}, "is_open"),
    ],
)
def open_admin_users_update_modal(
    update_icon_n_clicks,
    email,
    is_open,
):
    if update_icon_n_clicks:
        user = UserModel.find_by_email(email)
        return (
            not is_open,
            user.name,
            user.email,
            user.position,
            int(user.is_admin),
            user.holding,
            user.group,
            user.company,
            [auth_group.id for auth_group in user.authorization_groups],
        )
    return (is_open, "", "", "", "", "", "", "", [])


# ###############################################################################
# UPDATE USERS IN UPDATE MODAL
# ###############################################################################
@app.callback(
    Output(
        {"type": "update_user_will_be_updated_flag_div", "index": MATCH}, "children"
    ),
    Input({"type": "update_user_will_be_updated_btn", "index": MATCH}, "n_clicks"),
    [
        State({"type": "users-table-update-icon", "index": MATCH}, "value"),
        # The below is for updating the user
        State({"type": "user_will_be_updated_name", "index": MATCH}, "value"),
        State({"type": "user_will_be_updated_email", "index": MATCH}, "value"),
        State({"type": "user_will_be_updated_position", "index": MATCH}, "value"),
        State({"type": "is_user_will_be_updated_admin", "index": MATCH}, "value"),
        State({"type": "user_will_be_updated_holding", "index": MATCH}, "value"),
        State({"type": "user_will_be_updated_group", "index": MATCH}, "value"),
        State({"type": "user_will_be_updated_company", "index": MATCH}, "value"),
        State(
            {
                "type": "update_user_will_be_updated_authorization_groups_dropdown",
                "index": MATCH,
            },
            "value",
        ),
    ],
)
def open_admin_users_update_modal(
    update_user_btn_n_clicks,
    email,
    updated_name,
    updated_email,
    updated_position,
    updated_is_admin,
    updated_holding,
    updated_group,
    updated_company,
    updated_auth_groups,
):
    if update_user_btn_n_clicks:
        user = UserModel.find_by_email(email)
        user.name = updated_name
        user.email = updated_email
        user.position = updated_position
        user.is_admin = updated_is_admin
        user.holding = updated_holding
        user.group = updated_group
        user.company = updated_company
        user.authorization_groups = []
        for auth_group_id in updated_auth_groups:
            user.authorization_groups.append(
                AuthorizationGroupModel.find_by_id(auth_group_id)
            )
        user.save_to_db()
        return ""
