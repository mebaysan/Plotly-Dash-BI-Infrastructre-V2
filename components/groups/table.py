from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

from models.user import AuthorizationGroupModel, RoleModel


def get_auth_groups_table(auth_groups):
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
    for auth_group in auth_groups:
        rows.append(
            html.Tr(
                [
                    html.Td(auth_group.name),
                    html.Td(
                        html.Button(
                            html.Img(src="/assets/table-edit.png"),
                            id={
                                "type": "auth_groups-table-update-icon",
                                "index": auth_group.name,
                            },
                            style={"background-color": "white", "padding": "0px"},
                            value=str(auth_group.name),
                        )
                    ),
                    html.Td(
                        html.Button(
                            html.Img(src="/assets/table-close.png"),
                            id={
                                "type": "auth_groups-table-delete-icon",
                                "index": auth_group.name,
                            },
                            style={"background-color": "white", "padding": "0px"},
                            value=str(auth_group.name),
                        )
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(
                                dbc.ModalTitle(
                                    [
                                        html.Div(
                                            [
                                                html.H5(html.B("Update a Group")),
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
                                                            "type": "auth_group_will_be_updated_name",
                                                            "index": auth_group.name,
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
                                                        id={
                                                            "type": "update_auth_group_will_be_updated_authorization_groups_dropdown",
                                                            "index": auth_group.name,
                                                        },
                                                    ),
                                                    html.Br(),
                                                    dbc.Button(
                                                        children="Update Group",
                                                        id={
                                                            "type": "update_auth_group_will_be_updated_btn",
                                                            "index": auth_group.name,
                                                        },
                                                        n_clicks=0,
                                                        type="submit",
                                                        className="baysansoft-btn-active",
                                                    ),
                                                    html.Div(
                                                        id={
                                                            "type": "update_auth_group_will_be_updated_flag_div",
                                                            "index": auth_group.name,
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
                            "type": "auth_groups-admin-update-modal",
                            "index": auth_group.name,
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
