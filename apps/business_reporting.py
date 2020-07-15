import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from common import common_functions, constants
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json, uuid
import pandas as pd
import numpy as np
from app import app
import plotly.graph_objs as go
import plotly.express as px

def get_layout(args,search):

    df = pd.read_csv('data/data.csv')

    if args[0]['type'] == 'is_admin' and args[0]['value'] == True:
        filtered_df = df
    elif args[0]['type'] == 'user_id':
        filtered_df = df[ df[args[0]['type']] ==  int(args[0]['value']) ]
    else:
        filtered_df = pd.DataFrame(columns=['gender','enquiry_type','enquiry_month','uuid','conversion','user_id','is_admin'])


    enquiry_month_crostab = pd.crosstab(filtered_df['enquiry_month'],filtered_df['conversion']).reset_index()
    enquiry_month_crostab['FullDate'] = pd.to_datetime("01"+enquiry_month_crostab['enquiry_month'])
    enquiry_month_crostab = (enquiry_month_crostab.sort_values(by='FullDate',ascending=True)).drop(columns="FullDate")

    conversion_predicted = enquiry_month_crostab.copy()
    conversion_predicted['type'] = 'Actual'
    conversion_predicted.rename(columns={'enquiry_month':'Month'}, inplace=True)
    conversion_predicted.loc[len(conversion_predicted)] = ['Jul-2020',round(enquiry_month_crostab['Converted'].mean()),0,'Predicted']
    conversion_predicted.loc[len(conversion_predicted)] = ['Aug-2020',round(enquiry_month_crostab['Converted'].median()-1.5),0,'Predicted']
    conversion_predicted.loc[len(conversion_predicted)] = ['Sep-2020',round(enquiry_month_crostab['Converted'].mean()+2),0,'Predicted']

    fig = px.bar(conversion_predicted, x='Month', y='Converted', color='type',
             color_discrete_sequence=["goldenrod", "green"], text='Converted',
            )

    # Change the bar mode
    fig.update_layout(
    #     bargroupgap=0.1,
        plot_bgcolor="#F9F9F9",
        title_x = 0,
        # autosize=True,
        height= 600,
        margin=dict(
            l=20,
            r=5,
            b=20,
            t=50,
            pad=3
        ),
        xaxis = dict(
            tickangle = 0,
            title_text = "<b>Month</b>",
            title_font = {"size": 16},
            tickfont = {"size": 16},
        ),
        yaxis = dict(
            title_text = "<b>No. of Clients</b>",
            title_font = {"size": 16},
        ),
        legend = dict (
            title="",
            font = {"size": 16},
        ),
    )
    fig.update_traces(
        opacity=0.9,
        textposition='outside'
    )


    layout = html.Div(
        [
            dbc.Spinner(html.Div(id="home-loader"),color="success", spinner_style=constants.SPINNER_CLASS),
            common_functions.get_menu(args,search),
            html.Div(
            [
                html.Div(json.dumps(args), id="args", style={'display': 'none'}),
                html.H2("Business Reporting", className='text-center', style={"margin-bottom": "20px"}),

                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        html.Br(),
                        dbc.ListGroup(
                            [
                                dbc.ListGroupItem("Revenue Factors in last 3 months", style={'padding':'.5rem','font-size':'1.5rem', 'background-color':'#92509f', 'color':'#FFF'}),
                                dbc.ListGroupItem(f"Dropouts - {4}",style={'font-size':'1.1rem'}),
                                dbc.ListGroupItem(f"Lesser Conversions - {7}",style={'font-size':'1.1rem'}),
                            ]
                        ),
                        html.Br(),
                        html.Br(),
                        dbc.ListGroup(
                            [
                                dbc.ListGroupItem([
                                    html.Span("Top Non Conversion and Dropout Factors    "),
                                    html.I(className="fa fa-arrow-down fa-1x", **{'aria-hidden': 'true'}, children=None),
                                ], style={'padding':'.5rem','font-size':'1.5rem', 'background-color':'#92509f', 'color':'#FFF'}),
                                dbc.ListGroupItem("Lack of Funds / Unable to afford ", style={'font-size':'1.1rem'}),
                                dbc.ListGroupItem("Location",style={'font-size':'1.1rem'}),
                                dbc.ListGroupItem("Infrastructure",style={'font-size':'1.1rem'}),
                                
                            ]
                        )
                    ], width=4),
                    dbc.Col([
                        html.Div([
                            dbc.Col(
                                html.H4("Actual conversions each month vs No. of predicted conversions for next three months"  , style={"margin-bottom": "0px !important"}, className='text-center'),
                            ),
                            dcc.Graph(
                                id='enquiry-lead-graph',
                                figure=fig,
                                style={'height': '70vh'},
                                config={
                                    'displaylogo': False,
                                    # 'displayModeBar': True
                                }
                            )

                        ], style= {"margin-left": "20px", "margin-bottom": "20px", "margin-top": "20px" }
                        ),
                    ], lg=8),
                
                ])
            ], id="page-content")
        ])
    return layout





