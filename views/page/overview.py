# Dash Packages
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State

# Core App | you can bind your callbacks by using this variable
from app import app

###############################################################################
########### Overview PAGE LAYOUT ###########
###############################################################################


def get_layout(user):
    if not user.is_my_role("page-overview"):
        layout = "You have no permission to see this page..."
    else:
        layout = dbc.Container(
            [
                html.H2("Overview Layout"),
                html.Hr(),
                html.H3(
                    "If you see this page, you have `page-overview` permission. It is assigned into your roles."
                ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
            ],
            className="mt-4",
        )
    return layout


