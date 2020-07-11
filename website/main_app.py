# -*- coding: utf-8 -*-
"""Main Dash App."""
import dash
from flask_caching import Cache

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '__cache__',
})

app.title = "APAP Systems Inc."
