# -*- coding: utf-8 -*-
"""Loads different apps on different urls."""
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html

from main_app import app
from dashboards import business_contacts, empty_tab

tabs_styles = {
    'height': '70px',
    'fontSize': '22px',
}

tab_style = {}

tab_selected_style = {
    'fontWeight': 'bold',
}


layout = html.Div([
    html.H1('APAP Systems Inc.'),
    dcc.Tabs(
        id='tabs-selector',
        children=[
            dcc.Tab(label='Business - Gestion des contacts', value='tab-business-contacts', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab 2', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        ],
        value='tab-business-contacts',
        style=tabs_styles,
        persistence=True,
        persistence_type="session",
    ),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs-selector', 'value')])
def render_content(tab):
    """Organize tabs."""
    if tab == 'tab-business-contacts':
        return business_contacts.layout
    elif tab == 'tab-2':
        return empty_tab.layout
    else:
        return '404 not found'
