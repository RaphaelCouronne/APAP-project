# -*- coding: utf-8 -*-
"""AMS-IX display graphs."""

import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
from dash_table import DataTable
import pandas as pd

from server import app, cache
from assets.config import DEFAULT_COLORS as colors

import os
import pathlib
path_dir = pathlib.Path(__file__).parent.absolute()
path_proj = os.path.join(path_dir, "../..")

path_candidates = os.path.join(path_proj, 'data/processed/candidate_database.csv')


def generate_table(df, page_size=10):
    """Generate a formatted table from a DataFrame."""
    table = DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=page_size,
        style_cell={
            'textAlign': 'left',
            'color': "#000000"
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'count'},
                'textAlign': 'right'
            }
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    )
    return table


layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.Div(id='business-contacts-ix-main-page'),
        html.H1("Welcome"),
        html.Button("Push DT", id='push-dt', n_clicks=0),
        html.Button('Push Plan de Charge', id='push-plan-de-charge', n_clicks=0),

        html.Div(id='dropdown-menus', children=[
            dcc.Dropdown(id='secteur-dropdown',
                         placeholder="Selectionner un secteur d'activité",
                         multi=True,
                         value=[],
                         style={'textAlign': 'center', 'width': '40%', 'margin': 'auto'}),
            dcc.Dropdown(id='competences-dropdown',
                         placeholder="Selectionner une compétence métier",
                         multi=True,
                         value=[],
                         style={'textAlign': 'center', 'width': '40%', 'margin': 'auto'}),
            dcc.Dropdown(id='logiciel-dropdown',
                         placeholder="Selectionner un logiciel",
                         multi=True,
                         value=[],
                         style={'textAlign': 'center', 'width': '40%', 'margin': 'auto'}),
            # dcc.Dropdown(id='autres-dropdown',
            #              placeholder="Selectionner autres",
            #              multi=True,
            #              style={'textAlign': 'center', 'width': '40%', 'margin': 'auto'}),
        ]),

        html.Br(),
        html.Br(),
        html.P(id='debug'),
        html.Br(),
        html.Br(),

        html.Div(id="main-table", style={"width": "100%", "margin": "auto"}),


        dcc.Interval(id='business-contacts-interval',
                     interval=5*60*1000,  # 5 minutes (in milliseconds)
                     # interval=1*1000,  # in milliseconds
                     n_intervals=0)
    ]
)


@app.callback(
    [Output('secteur-dropdown', 'options'),
     Output('competences-dropdown', 'options'),
     Output('logiciel-dropdown', 'options'),
     # Output('autres-dropdown', 'options')],
     ],
    [Input('business-contacts-interval', 'n_intervals')]
)
def update_dropdown(n_intervals):
    """Update dropdown based on values."""
    df = pd.read_csv(path_candidates, index_col=0)

    secteurs = df.branch.value_counts().index.tolist()
    jobs = df.job.value_counts().index.tolist()
    logiciels = df[["R", "Simulink", "Python", "Matlab", "Java", "C++"]].columns.tolist()

    secteurs_options = []
    for secteur in secteurs:
        secteurs_options.append(
            dict(
                label="secteur/" + secteur,
                value=secteur
            )
        )

    jobs_options = []
    for job in jobs:
        jobs_options.append(
            dict(
                label="job/" + job,
                value=job
            )
        )

    logiciels_options = []
    for logiciel in logiciels:
        logiciels_options.append(
            dict(
                label="logiciel/" + logiciel,
                value=logiciel
            )
        )
    print(secteurs_options)
    return secteurs_options, jobs_options, logiciels_options  # , autres_options


@app.callback(
    Output('debug', 'children'),
    [Input('secteur-dropdown', 'value'),
     Input('competences-dropdown', 'value'),
     Input('logiciel-dropdown', 'value'),
     # Input('autres-dropdown', 'value')]
     ]
)
def debug_1(secteurs, competences, logiciels):
    return str(secteurs) + str(competences) + str(logiciels)


@app.callback(
    Output('main-table', 'children'),
    [Input('secteur-dropdown', 'value'),
     Input('competences-dropdown', 'value'),
     Input('logiciel-dropdown', 'value'),
     # Input('autres-dropdown', 'value')]
     ]
)
def update_table(secteurs, competences, logiciels):  # , autres):
    """Show table."""
    df_full = pd.read_csv(path_candidates, index_col=0)
    df = df_full.copy()

    if secteurs == [] and competences == [] and logiciels == []:
        return generate_table(df_full, page_size=30)

    if secteurs != []:
        df = df[df.branch.isin(secteurs)]

    if competences != []:
        df = df[df.job.isin(competences)]

    if logiciels != []:
        for logiciel in logiciels:
            df = df[df[logiciel] == 1]
    return generate_table(df)
