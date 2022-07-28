from dash import dcc, html, dash_table as dt
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State, ALL, MATCH

from app import app
from models.user import AuthorizationGroupModel, AuthorizationGroupModel, RoleModel

from components.core.page import header
from components.groups.table import get_auth_groups_table


import time


def get_layout(user):
    ROW_MARGIN_TOP = "50px"
    layout = dbc.Container(
        [
            header("Group & Access Management", "Management Dashboard"),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Input(
                                placeholder="Search in groups...",
                                style={"width": "280px", "height": "40px"},
                                id="search-in-auth_groups-text",
                                n_submit=0,
                            ),
                            html.Button(
                                "Search",
                                className="baysansoft-btn-active",
                                style={"width": "75px", "margin-left": "15px"},
                                id="search-in-auth_groups-btn",
                                n_clicks=0,
                            ),
                            html.Button(
                                "Add Group Access",
                                className="baysansoft-btn-active",
                                style={"width": "160px", "float": "right"},
                                id="auth_groups-admin-add-modal-open-btn",
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
                                                            html.B("Create a Group")
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
                                                                id="new_auth_group_name",
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
                                                            dbc.Label("Roles "),
                                                            dcc.Dropdown(
                                                                options=[
                                                                    {
                                                                        "label": role.name,
                                                                        "value": role.id,
                                                                    }
                                                                    for role in RoleModel.get_all()
                                                                ],
                                                                multi=True,
                                                                id="new_auth_group_auth_groups",
                                                            ),
                                                            html.Br(),
                                                            dbc.Button(
                                                                children="Create Group",
                                                                id="create_new_auth_group_btn",
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
                                id="auth_groups-admin-add-modal-open-modal",
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
                            html.Div(id="admin_auth_groups_auth_groups_table-div"),
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
# OPEN auth_group ADD MODAL
################################################################################
@app.callback(
    Output("auth_groups-admin-add-modal-open-modal", "is_open"),
    [
        Input("auth_groups-admin-add-modal-open-btn", "n_clicks"),
        Input("create_new_auth_group_btn", "n_clicks"),
    ],
)
def toggle_modal(n1, n2):
    if n1 > 0 or n2 > 0:
        return True
    return False


################################################################################
# CREATE auth_group BUTTON CLICKED - UPDATE DATABASE WITH NEW auth_group
################################################################################
@app.callback(
    [
        Output("admin_auth_groups_auth_groups_table-div", "children"),
        Output("create_new_auth_group_btn", "n_clicks"),
        Output("search-in-auth_groups-btn", "n_clicks"),
        Output("search-in-auth_groups-text", "n_submit"),
        Output("auth_groups-admin-add-modal-open-btn", "n_clicks"),
        # Clear form
        Output("search-in-auth_groups-text", "value"),
        Output("new_auth_group_name", "value"),
        Output("new_auth_group_auth_groups", "value"),
    ],
    [
        Input("create_new_auth_group_btn", "n_clicks"),
        # to search in auth_groups
        Input("search-in-auth_groups-btn", "n_clicks"),
        Input("search-in-auth_groups-text", "n_submit"),
        # to delete auth_group
        Input({"type": "auth_groups-table-delete-icon", "index": ALL}, "n_clicks"),
        # to refresh the table after updating a auth_group
        Input(
            {"type": "update_auth_group_will_be_updated_btn", "index": ALL}, "n_clicks"
        ),
    ],
    [
        State({"type": "auth_groups-table-delete-icon", "index": ALL}, "value"),
        State("search-in-auth_groups-text", "value"),
        State("new_auth_group_name", "value"),
        State("new_auth_group_auth_groups", "value"),
    ],
)
def create_auth_group_modal_refresh_auth_groups_table(
    n_clicks,
    n_clicks2,
    n_submit,
    delete_icon_n_clicks,
    update_auth_group_modal_btn_n_clicks,
    delete_icon_values,
    search_in_auth_groups_text,
    new_auth_group_name,
    new_auth_group_roles,
):
    if n_clicks > 0:
        # create a new auth_group
        try:
            new_auth_group = AuthorizationGroupModel(
                new_auth_group_name,
            )

            for role_id in new_auth_group_roles:
                role = RoleModel.find_by_id(role_id)
                new_auth_group.roles.append(role)

            new_auth_group.save_to_db()

            return (
                get_auth_groups_table(AuthorizationGroupModel.get_all()),
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
                get_auth_groups_table(AuthorizationGroupModel.get_all()),
                0,
                0,
                0,
                0,
                "",
                "",
                [],
            )

    if n_clicks2 > 0 or n_submit > 0:
        # search in auth_groups
        return (
            get_auth_groups_table(
                AuthorizationGroupModel.query.filter(
                    AuthorizationGroupModel.name.contains(search_in_auth_groups_text)
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

    if (
        1 in update_auth_group_modal_btn_n_clicks
        and update_auth_group_modal_btn_n_clicks != []
    ):
        time.sleep(0.1)  # asenkron probleminden dolayı burada sleep yaptık
        return (
            get_auth_groups_table(AuthorizationGroupModel.get_all()),
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
            AuthorizationGroupModel.find_by_name(name).delete_from_db()
            return (
                get_auth_groups_table(AuthorizationGroupModel.get_all()),
                0,
                0,
                0,
                0,
                "",
                "",
                [],
            )

    return (
        get_auth_groups_table(AuthorizationGroupModel.get_all()),
        0,
        0,
        0,
        0,
        "",
        "",
        [],
    )


################################################################################
# OPEN auth_group UPDATE MODAL & LOAD auth_group INFO TO FORM
################################################################################
@app.callback(
    Output({"type": "auth_groups-admin-update-modal", "index": MATCH}, "is_open"),
    Output({"type": "auth_group_will_be_updated_name", "index": MATCH}, "value"),
    Output(
        {
            "type": "update_auth_group_will_be_updated_authorization_groups_dropdown",
            "index": MATCH,
        },
        "value",
    ),
    [
        Input({"type": "auth_groups-table-update-icon", "index": MATCH}, "n_clicks"),
    ],
    [
        State({"type": "auth_groups-table-update-icon", "index": MATCH}, "value"),
        State({"type": "auth_groups-admin-update-modal", "index": MATCH}, "is_open"),
    ],
)
def open_admin_auth_groups_update_modal(
    update_icon_n_clicks,
    name,
    is_open,
):
    if update_icon_n_clicks:
        auth_group = AuthorizationGroupModel.find_by_name(name)
        return (
            not is_open,
            auth_group.name,
            [role.id for role in auth_group.roles],
        )
    return (is_open, "", [])


# ###############################################################################
# UPDATE auth_groupS IN UPDATE MODAL
# ###############################################################################
@app.callback(
    Output(
        {"type": "update_auth_group_will_be_updated_flag_div", "index": MATCH},
        "children",
    ),
    Input(
        {"type": "update_auth_group_will_be_updated_btn", "index": MATCH}, "n_clicks"
    ),
    [
        State({"type": "auth_groups-table-update-icon", "index": MATCH}, "value"),
        # The below is for updating the auth_group
        State({"type": "auth_group_will_be_updated_name", "index": MATCH}, "value"),
        State(
            {
                "type": "update_auth_group_will_be_updated_authorization_groups_dropdown",
                "index": MATCH,
            },
            "value",
        ),
    ],
)
def open_admin_auth_groups_update_modal(
    update_auth_group_btn_n_clicks,
    name,
    updated_name,
    updated_roles,
):
    if update_auth_group_btn_n_clicks:
        auth_group = AuthorizationGroupModel.find_by_name(name)
        auth_group.name = updated_name
        auth_group.roles = []
        for role in updated_roles:
            auth_group.roles.append(RoleModel.find_by_id(role))

        auth_group.save_to_db()

        return ""
