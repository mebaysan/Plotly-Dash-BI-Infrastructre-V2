# Dash Packages
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, no_update


def header(main_header, sub_header):
    return html.Div(
        [html.H2(html.B(main_header)), html.H3(sub_header)],
        className="core-page-header-div",
    )
