from dash import dcc, html, dash_table as dt
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State, ALL, MATCH

from app import app
from models.user import AuthorizationGroupModel, RoleModel

from components.core.page import header
from components.roles.table import get_roles_table


import time


def get_layout(user):
    ROW_MARGIN_TOP = "50px"
    layout = dbc.Container(
        [
            header("Role & Access Management", "Management Dashboard"),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Input(
                                placeholder="Search in roles...",
                                style={"width": "280px", "height": "40px"},
                                id="search-in-roles-text",
                                n_submit=0,
                            ),
                            html.Button(
                                "Search",
                                className="baysansoft-btn-active",
                                style={"width": "75px", "margin-left": "15px"},
                                id="search-in-roles-btn",
                                n_clicks=0,
                            ),
                            html.Button(
                                "Add role Access",
                                className="baysansoft-btn-active",
                                style={"width": "160px", "float": "right"},
                                id="roles-admin-add-modal-open-btn",
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
                                                            html.B("Create a Role")
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
                                                            dbc.Label("Name "),
                                                            dcc.Input(
                                                                id="new_role_name",
                                                                className="form-control",
                                                                n_submit=0,
                                                                style={"width": "90%"},
                                                            ),
                                                            html.Br(),
                                                        ],
                                                        className="col-6",
                                                    ),
                                                    html.Div(
                                                        [
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
                                                                id="new_role_auth_groups",
                                                            ),
                                                            html.Br(),
                                                            dbc.Button(
                                                                children="Create role",
                                                                id="create_new_role_btn",
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
                                id="roles-admin-add-modal-open-modal",
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
                            html.Div(id="admin_roles_roles_table-div"),
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
# OPEN ROLE ADD MODAL
################################################################################
@app.callback(
    Output("roles-admin-add-modal-open-modal", "is_open"),
    [
        Input("roles-admin-add-modal-open-btn", "n_clicks"),
        Input("create_new_role_btn", "n_clicks"),
    ],
)
def toggle_modal(n1, n2):
    if n1 > 0 or n2 > 0:
        return True
    return False


################################################################################
# CREATE ROLE BUTTON CLICKED - UPDATE DATABASE WITH NEW ROLE
################################################################################
@app.callback(
    [
        Output("admin_roles_roles_table-div", "children"),
        Output("create_new_role_btn", "n_clicks"),
        Output("search-in-roles-btn", "n_clicks"),
        Output("search-in-roles-text", "n_submit"),
        Output("roles-admin-add-modal-open-btn", "n_clicks"),
        # Clear form
        Output("search-in-roles-text", "value"),
        Output("new_role_name", "value"),
        Output("new_role_auth_groups", "value"),
    ],
    [
        Input("create_new_role_btn", "n_clicks"),
        # to search in roles
        Input("search-in-roles-btn", "n_clicks"),
        Input("search-in-roles-text", "n_submit"),
        # to delete role
        Input({"type": "roles-table-delete-icon", "index": ALL}, "n_clicks"),
        # to refresh the table after updating a role
        Input({"type": "update_role_will_be_updated_btn", "index": ALL}, "n_clicks"),
    ],
    [
        State({"type": "roles-table-delete-icon", "index": ALL}, "value"),
        State("search-in-roles-text", "value"),
        State("new_role_name", "value"),
        State("new_role_auth_groups", "value"),
    ],
)
def create_role_modal_refresh_roles_table(
    n_clicks,
    n_clicks2,
    n_submit,
    delete_icon_n_clicks,
    update_role_modal_btn_n_clicks,
    delete_icon_values,
    search_in_roles_text,
    new_role_name,
    new_role_auth_groups,
):
    if n_clicks > 0:
        # create a new role
        try:
            new_role = RoleModel(
                new_role_name,
            )
            new_role.save_to_db()

            for auth_group_id in new_role_auth_groups:
                auth_group = AuthorizationGroupModel.find_by_id(auth_group_id)
                auth_group.roles.append(new_role)
                auth_group.save_to_db()

            new_role.save_to_db()

            return (
                get_roles_table(RoleModel.get_all()),
                0,
                0,
                0,
                0,
                "",
                "",
                [],
            )
        except Exception as e:
            return (
                get_roles_table(RoleModel.get_all()),
                0,
                0,
                0,
                0,
                "",
                "",
                [],
            )

    if n_clicks2 > 0 or n_submit > 0:
        # search in roles
        return (
            get_roles_table(
                RoleModel.query.filter(
                    RoleModel.name.contains(search_in_roles_text)
                ).all()
            ),
            0,
            0,
            0,
            0,
            "",
            "",
            [],
        )

    if 1 in update_role_modal_btn_n_clicks and update_role_modal_btn_n_clicks != []:
        time.sleep(0.1)  # asenkron probleminden dolayı burada sleep yaptık
        return (
            get_roles_table(RoleModel.get_all()),
            0,
            0,
            0,
            0,
            "",
            "",
            [],
        )

    if len(delete_icon_n_clicks) > 0:
        if 1 in delete_icon_n_clicks:
            index = delete_icon_n_clicks.index(1)
            name = delete_icon_values[index]
            RoleModel.find_by_name(name).delete_from_db()
            return (
                get_roles_table(RoleModel.get_all()),
                0,
                0,
                0,
                0,
                "",
                "",
                [],
            )

    return (
        get_roles_table(RoleModel.get_all()),
        0,
        0,
        0,
        0,
        "",
        "",
        [],
    )


################################################################################
# OPEN role UPDATE MODAL & LOAD role INFO TO FORM
################################################################################
@app.callback(
    Output({"type": "roles-admin-update-modal", "index": MATCH}, "is_open"),
    Output({"type": "role_will_be_updated_name", "index": MATCH}, "value"),
    Output(
        {
            "type": "update_role_will_be_updated_authorization_groups_dropdown",
            "index": MATCH,
        },
        "value",
    ),
    [
        Input({"type": "roles-table-update-icon", "index": MATCH}, "n_clicks"),
    ],
    [
        State({"type": "roles-table-update-icon", "index": MATCH}, "value"),
        State({"type": "roles-admin-update-modal", "index": MATCH}, "is_open"),
    ],
)
def open_admin_roles_update_modal(
    update_icon_n_clicks,
    name,
    is_open,
):
    if update_icon_n_clicks:
        role = RoleModel.find_by_name(name)
        auth_groups = AuthorizationGroupModel.query.filter(
            AuthorizationGroupModel.roles.contains(role)
        ).all()
        return (
            not is_open,
            role.name,
            [auth_group.id for auth_group in auth_groups],
        )
    return (is_open, "", [])


# ###############################################################################
# UPDATE ROLES IN UPDATE MODAL
# ###############################################################################
@app.callback(
    Output(
        {"type": "update_role_will_be_updated_flag_div", "index": MATCH}, "children"
    ),
    Input({"type": "update_role_will_be_updated_btn", "index": MATCH}, "n_clicks"),
    [
        State({"type": "roles-table-update-icon", "index": MATCH}, "value"),
        # The below is for updating the role
        State({"type": "role_will_be_updated_name", "index": MATCH}, "value"),
        State(
            {
                "type": "update_role_will_be_updated_authorization_groups_dropdown",
                "index": MATCH,
            },
            "value",
        ),
    ],
)
def open_admin_roles_update_modal(
    update_role_btn_n_clicks,
    name,
    updated_name,
    updated_auth_groups,
):
    if update_role_btn_n_clicks:
        role = RoleModel.find_by_name(name)
        role.name = updated_name
        role.save_to_db()

        # firstly remove the old groups are connected with the role
        auth_groups = AuthorizationGroupModel.query.filter(
            AuthorizationGroupModel.roles.contains(role)
        )
        for auth_group in auth_groups:
            auth_group.roles.remove(role)
            auth_group.save_to_db()

        # then create new connections between the role and the groups
        for auth_group_id in updated_auth_groups:
            auth_group = AuthorizationGroupModel.find_by_id(auth_group_id)
            auth_group.roles.append(role)
            auth_group.save_to_db()

        return ""
