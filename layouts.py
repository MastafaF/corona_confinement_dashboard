import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from data import (
    country_labels, time_series_date_list, dates, date_strings, city_Sweden_labels, compute_correlation
    )
from model import ndays
import numpy as np

pandemic_tab = html.Div([
    html.Div([
        html.P('Variable sorting method:'),
        html.Div([dcc.RadioItems(
                id='charlie-sort',
                options=[{'label': i, 'value': i} for i in ['Regular Sort', 'Charlie Sort']],
                value='Regular Sort',
                labelStyle={'display': 'inline-block', 'margin-right':10}
            )],style={
                'margin':'10 auto',
                'borderBottom': 'thin lightgrey solid',
                'backgroundColor': 'rgb(250, 250, 250)',
                'padding': '5px 10px'}),
        html.Br(),
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                # options=[{'label':labels[label], 'value':label} for label in list(labels.keys())],
                value='confirmed',
            ),
            html.Br(),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Log',
                labelStyle={'display': 'inline-block', 'margin-right':10}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                # options=[{'label':labels[label], 'value':label} for label in labels],
                value='deaths'
            ),
            html.Br(),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Log',
                labelStyle={'display': 'inline-block', 'margin-right':10}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '0px 10px'
        }
    ),
    html.Div(dcc.Slider(
        id='crossfilter-date--slider',
        min=0,
        max=np.arange(len(date_strings)).max(),
        step=1,
        value=np.arange(len(date_strings)).max(),
        marks={
            0: date_strings[0],
            13: date_strings[13],
            27: date_strings[27],
            41: date_strings[41],
            int(np.arange(len(date_strings)).max()): date_strings[-1]
        },
        updatemode='drag'
        ), style={'width': '80%', 'padding': '20px 20px 20px 20px', 'margin':'0 auto'}),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'US'}]},
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),
],style={'width':'80%','margin':'0 auto'})


global_tab = html.Div(children=[
    html.H3(children=[
        'Select a Country'],style={'width':'30%','margin':'0 auto'}),
    html.Div(children=[
            dcc.Dropdown(
                id='global-dropdown',
                options=country_labels,
                value='Global'
            )],style={'width':'30%', 'margin':'0 auto'}),
    html.Div(children=[dcc.Graph(id='global-graph')],style={'width':'80%','margin':'0 auto'}),
    html.Div(children=[dcc.Graph(id='global-daily-graph')],style={'width':'80%','margin':'0 auto'})
    # html.Div(
    # 	children=[dcc.Graph(id='combo-graph')],
    # 	style={'width':'80%','margin':'0 auto'}
    # )
    ])



# @TODO: add our own tab here --> update data.py
confinement_tab = html.Div(children=[
    html.H3(children=[
        'Select a City'],style={'width':'30%','margin':'0 auto'}),
    html.Div(children=[
            dcc.Dropdown(
                id='confinement-dropdown',
                options=city_Sweden_labels,
                value='Stockholm'
            )],style={'width':'30%', 'margin':'0 auto'}),
    html.Div(children=[dcc.Graph(id='confinement-daily-graph')],style={'width':'80%','margin':'0 auto'}),
    html.Div(children=[dcc.Graph(id='confinement-graph')],style={'width':'80%','margin':'0 auto'})
    # html.Div(
    # 	children=[dcc.Graph(id='combo-graph')],
    # 	style={'width':'80%','margin':'0 auto'}
    # )
    ])

confinement_yesterday_tab = html.Div(children=[
    html.H3(children=[
        'Select a City'],style={'width':'30%','margin':'0 auto'}),
    html.Div(children=[
            dcc.Dropdown(
                id='confinement-hourly-dropdown',
                options=city_Sweden_labels,
                value='Stockholm'
            )],style={'width':'30%', 'margin':'0 auto'}),
    html.Div(children=[dcc.Graph(id='confinement-hourly-graph')],style={'width':'80%','margin':'0 auto'}),
    # html.Div(
    # 	children=[dcc.Graph(id='combo-graph')],
    # 	style={'width':'80%','margin':'0 auto'}
    # )
    ])

analysis_tab = html.Div(children=[
    html.H3(children=[
        'Select a City'],style={'width':'30%','margin':'0 auto'}),
    html.Div(children=[
            dcc.Dropdown(
                id='analysis-dropdown',
                options=city_Sweden_labels,
                value='Stockholm'
            )],
            style={'width':'30%', 'margin':'0 auto'}),

    html.Div(children=[dcc.Markdown(id='correlation')],style={'width':'80%','margin':'0 auto', 'color':'red', 'font-size': 'large', 'border ': '3px solid red' }),

    html.Div(children=[dcc.Graph(id='analysis-graph')],style={'width':'80%','margin':'0 auto'})
    ])
