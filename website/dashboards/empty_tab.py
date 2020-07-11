# -*- coding: utf-8 -*-
"""AMS-IX display graphs."""

import dash_core_components as dcc
import dash_html_components as html

from assets.config import DEFAULT_COLORS as colors


layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.Div(id='empty-page'),
        dcc.Interval(id='empty-page-interval',
                     interval=5*60*1000,  # 5 minutes (in milliseconds)
                     # interval=1*1000,  # in milliseconds
                     n_intervals=0)
    ]
)
