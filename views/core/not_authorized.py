"""
    Route şemasında eğer rol tanımlı değilse direkt buraya yönlendirilsin olarak düşünüldü. Henüz üzerinde çalışılmadı.
"""
# Dash packages
import dash_bootstrap_components as dbc
from dash import html

from app import app

###############################################################################
########### Overview PAGE LAYOUT ###########
###############################################################################


def get_layout(user, role):
    layout = dbc.Container(
        [
            html.H2("Non-Authorized Layout"),
            html.Hr(),
            html.H3(
                f"Bu sayfayı görüyorsanız `{role}` rolleriniz içerisinde tanımlı değildir"
            ),
        ],
        className="mt-4",
    )
    return layout
