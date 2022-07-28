# Dash Packages
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, no_update


def card(_title, _children, _is_title_left=True, _title_id=""):
    """Generates a card component with the given children

    This card has to be wrapped with column.

    Args:
        _title (str): It will be written in the H1 if it's not != ''
        _children (list): List of components
        _is_title_left (bool, optional): If it's false, float will be right. Defaults to True.
        _title_id (str, optional): In the future, maybe we want to put dynamic content inside it. Defaults to "".

    Returns:
        html.Div: Generates a div
    
    Example:
        html.Div([
            html.Div([
                card('Card Title', [html.Div([
                    html.Div([
                        go.Figure()
                    ],className='col')
                ],className='row')])
            ],className='col')
        ],className='row')
    """
    title_div_style = {}
    title_div_style["display"] = "none" if _title == "" else ""

    title_style = {}
    title_style["float"] = "left" if _is_title_left == True else "right"

    return html.Div(
        [
            html.Div(
                [html.H1(_title, id=_title_id, style=title_style)],
                className="vagon-card-header",
                style=title_div_style,
            ),
            html.Div(
                _children,
                className="vagon-card-content",
            ),
        ],
        className="vagon-card",
    )
