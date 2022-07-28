from dash import dcc, html
import dash_bootstrap_components as dbc

from app import app

layout = dbc.Container(
    [
        html.Br(),
        dbc.Container(
            [
                dcc.Location(id="err404", refresh=True),
                dbc.Container(
                    html.Img(src="/assets/logo-black.png", className="center"),
                ),
                dbc.Container(
                    [
                        dbc.Container(
                            id="outputState", children="Error 404 - Page not found"
                        )
                    ],
                    className="form-group",
                ),
            ],
            className="jumbotron",
        ),
    ]
)
