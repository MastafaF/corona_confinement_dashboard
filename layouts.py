import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from data import (
    country_labels, time_series_date_list, dates, date_strings, city_Sweden_labels, compute_correlation
    )
from model import ndays
import numpy as np

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



