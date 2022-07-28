from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

from models.user import AuthorizationGroupModel


def get_roles_table(roles):
    headers = [
        "Name",
        "",
        "",
    ]
    table_header = [
        html.Thead(
            html.Tr(
                [html.Th(th) for th in headers], style={"border": "2px white solid"}
            )
        )
    ]

    rows = []
    for role in roles:
        rows.append(
            html.Tr(
                [
                    html.Td(role.name),
                    html.Td(
                        html.Button(
                            html.Img(src="/assets/table-edit.png"),
                            id={"type": "roles-table-update-icon", "index": role.name},
                            style={"background-color": "white", "padding": "0px"},
                            value=str(role.name),
                        )
                    ),
                    html.Td(
                        html.Button(
                            html.Img(src="/assets/table-close.png"),
                            id={"type": "roles-table-delete-icon", "index": role.name},
                            style={"background-color": "white", "padding": "0px"},
                            value=str(role.name),
                        )
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(
                                dbc.ModalTitle(
                                    [
                                        html.Div(
                                            [
                                                html.H5(html.B("Update a Role")),
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
                                                        id={
                                                            "type": "role_will_be_updated_name",
                                                            "index": role.name,
                                                        },
                                                        className="form-control",
                                                        n_submit=0,
                                                        style={"width": "90%"},
                                                    ),
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
                                                        id={
                                                            "type": "update_role_will_be_updated_authorization_groups_dropdown",
                                                            "index": role.name,
                                                        },
                                                    ),
                                                    html.Br(),
                                                    dbc.Button(
                                                        children="Update role",
                                                        id={
                                                            "type": "update_role_will_be_updated_btn",
                                                            "index": role.name,
                                                        },
                                                        n_clicks=0,
                                                        type="submit",
                                                        className="baysansoft-btn-active",
                                                    ),
                                                    html.Div(
                                                        id={
                                                            "type": "update_role_will_be_updated_flag_div",
                                                            "index": role.name,
                                                        },
                                                        style={"display": "none"},
                                                    ),
                                                ],
                                                className="col-6",
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ],
                        id={
                            "type": "roles-admin-update-modal",
                            "index": role.name,
                        },
                        size="lg",
                        is_open=False,
                    ),
                ]
            )
        )

    table_body = [html.Tbody(rows)]

    table = dbc.Table(
        table_header + table_body,
        bordered=False,
        style={"background-color": "white", "font-family": "IBM Plex Mono"},
    )
    return table
