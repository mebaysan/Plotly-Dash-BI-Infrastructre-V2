from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

from models.user import AuthorizationGroupModel


def get_users_table(users):
    headers = [
        "Name",
        "Position",
        "Group",
        "Company",
        "Email",
        "Created Date",
        "Updated Date",
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
    for user in users:
        rows.append(
            html.Tr(
                [
                    html.Td(user.name),
                    html.Td(user.position),
                    html.Td(user.group),
                    html.Td(user.company),
                    html.Td(user.email),
                    html.Td(datetime.strftime(user.created_date, "%d.%m.%Y")),
                    html.Td(datetime.strftime(user.updated_date, "%d.%m.%Y")),
                    html.Td(
                        html.Button(
                            html.Img(src="/assets/table-edit.png"),
                            id={"type": "users-table-update-icon", "index": user.email},
                            style={"background-color": "white", "padding": "0px"},
                            value=str(user.email),
                        )
                    ),
                    html.Td(
                        html.Button(
                            html.Img(src="/assets/table-close.png"),
                            id={"type": "users-table-delete-icon", "index": user.email},
                            style={"background-color": "white", "padding": "0px"},
                            value=str(user.email),
                        )
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(
                                dbc.ModalTitle(
                                    [
                                        html.Div(
                                            [
                                                html.H5(html.B("Update an Account")),
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
                                                        id={
                                                            "type": "user_will_be_updated_name",
                                                            "index": user.email,
                                                        },
                                                        className="form-control",
                                                        n_submit=0,
                                                        style={"width": "90%"},
                                                    ),
                                                    html.Br(),
                                                    dbc.Label("Email Address"),
                                                    dcc.Input(
                                                        id={
                                                            "type": "user_will_be_updated_email",
                                                            "index": user.email,
                                                        },
                                                        type="email",
                                                        className="form-control",
                                                        n_submit=0,
                                                        style={"width": "90%"},
                                                    ),
                                                    html.Br(),
                                                    dbc.Label("Position "),
                                                    dcc.Input(
                                                        id={
                                                            "type": "user_will_be_updated_position",
                                                            "index": user.email,
                                                        },
                                                        className="form-control",
                                                        n_submit=0,
                                                        style={"width": "90%"},
                                                    ),
                                                    html.Br(),
                                                    dbc.Label("Admin "),
                                                    dcc.Dropdown(
                                                        id={
                                                            "type": "is_user_will_be_updated_admin",
                                                            "index": user.email,
                                                        },
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
                                                ],
                                                className="col-6",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Holding "),
                                                    dcc.Input(
                                                        id={
                                                            "type": "user_will_be_updated_holding",
                                                            "index": user.email,
                                                        },
                                                        className="form-control",
                                                        n_submit=0,
                                                        style={"width": "90%"},
                                                    ),
                                                    html.Br(),
                                                    dbc.Label("Group "),
                                                    dcc.Input(
                                                        id={
                                                            "type": "user_will_be_updated_group",
                                                            "index": user.email,
                                                        },
                                                        className="form-control",
                                                        n_submit=0,
                                                        style={"width": "90%"},
                                                    ),
                                                    html.Br(),
                                                    dbc.Label("Company "),
                                                    dcc.Input(
                                                        id={
                                                            "type": "user_will_be_updated_company",
                                                            "index": user.email,
                                                        },
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
                                                        id={
                                                            "type": "update_user_will_be_updated_authorization_groups_dropdown",
                                                            "index": user.email,
                                                        },
                                                    ),
                                                    html.Br(),
                                                    dbc.Button(
                                                        children="Update User",
                                                        id={
                                                            "type": "update_user_will_be_updated_btn",
                                                            "index": user.email,
                                                        },
                                                        n_clicks=0,
                                                        type="submit",
                                                        className="baysansoft-btn-active",
                                                    ),
                                                    html.Div(
                                                        id={
                                                            "type": "update_user_will_be_updated_flag_div",
                                                            "index": user.email,
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
                            "type": "users-admin-update-modal",
                            "index": user.email,
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
