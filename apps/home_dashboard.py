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


def get_layout(args,search):

    df = pd.read_csv('data/data.csv')

    if args[0]['type'] == 'is_admin' and args[0]['value'] == True:
        filtered_df = df
    elif args[0]['type'] == 'user_id':
        filtered_df = df[ df[args[0]['type']] ==  int(args[0]['value']) ]
    else:
        filtered_df = pd.DataFrame(columns=['gender','enquiry_type','enquiry_month','uuid','conversion','user_id','is_admin'])


    enquiry_type_crostab = pd.crosstab(filtered_df['enquiry_type'],filtered_df['conversion']).reset_index()
    enquiry_lead_figure = go.Figure(data=[
                            go.Bar(
                                name='Enquiry Only', 
                                x=enquiry_type_crostab['enquiry_type'], 
                                y=enquiry_type_crostab['Enquiry'],
                                marker_color='rgb(255, 153, 0)'
                            ),
                            go.Bar(
                                name='Converted',
                                x=enquiry_type_crostab['enquiry_type'], 
                                y=enquiry_type_crostab['Converted'],
                                marker_color='rgb(146, 80, 159)'
                            )
                        ])

    # Change the bar mode
    enquiry_lead_figure.update_layout(
        barmode='group',
    #     bargroupgap=0.1,
        plot_bgcolor="#F9F9F9",
        title_x = 0,
        # autosize=True,
        height= 600,
        margin=dict(
            l=20,
            r=5,
            b=20,
            t=20,
            pad=3
        ),
        xaxis = dict(
            tickangle = 0,
            title_text = "<b>Lead Type</b>",
            title_font = {"size": 15},
            tickfont = {"size": 10},
        ),
        yaxis = dict(
            title_text = "<b>No. of Clients</b>",
            title_font = {"size": 15},
            hoverformat = '..2f'
        ),
        legend = dict (
            x=0,
            y=-.15,    
            orientation="h",
            yanchor= "bottom",
            xanchor="auto",
            # placement="bottom bottom"
        ),
        separators= '.,',
    )
    enquiry_lead_figure.update_traces(
        hovertemplate = "%{x}: <br> %{y}%",
        opacity=0.9
    )


    enq_month_crostab = pd.crosstab(filtered_df['enquiry_month'],filtered_df['conversion']).reset_index()
    enq_month_crostab['FullDate'] = pd.to_datetime("01"+enq_month_crostab['enquiry_month'])
    enq_month_crostab = (enq_month_crostab.sort_values(by='FullDate',ascending=True)).drop(columns="FullDate")

    enq_month_fig = go.Figure(data=[
        go.Bar(
            name='Enquiry Only', 
            x=enq_month_crostab['enquiry_month'], 
            y=enq_month_crostab['Enquiry'],
            marker_color='rgb(255, 153, 0)'
        ),
        go.Bar(
            name='Converted',
            x=enq_month_crostab['enquiry_month'], 
            y=enq_month_crostab['Converted'],
            marker_color='rgb(146, 80, 159)'
        )      
    ])
    enq_month_fig.update_layout(
        barmode='group',
    #     bargroupgap=0.1,
        plot_bgcolor="#F9F9F9",
        title_x = 0,
        # autosize=True,
        height= 600,
        margin=dict(
            l=20,
            r=5,
            b=20,
            t=20,
            pad=3
        ),
        xaxis = dict(
            tickangle = 0,
            title_text = "<b>Enquiry Month</b>",
            title_font = {"size": 15},
            tickfont = {"size": 10},
        ),
        yaxis = dict(
            title_text = "<b>No. of Clients</b>",
            title_font = {"size": 15},
            hoverformat = '..2f'
        ),
        legend = dict (
            x=0,
            y=-.15,    
            orientation="h",
            yanchor= "bottom",
            xanchor="auto",
            # placement="bottom bottom"
        ),
        separators= '.,',
    )
    enq_month_fig.update_traces(
        hovertemplate = "%{x}: <br> %{y}%",
        # marker_color='rgba(128, 0, 128, 0.6)', marker_line_color='rgba(128, 0, 128, 1)',  
        opacity=0.9
    )


    layout = html.Div(
        [
            dbc.Spinner(html.Div(id="home-loader"),color="success", spinner_style=constants.SPINNER_CLASS),
            common_functions.get_menu(args,search),
            html.Div(
            [
                html.Div(json.dumps(args), id="args", style={'display': 'none'}),
                html.H2("Dashboard", className='text-center', style={"margin-bottom": "20px"}),
                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.I(className="fa fa-question-circle fa-8x", **{'aria-hidden': 'true'}, children=None), 
                                                width={"size": 3}, align="center"
                                            ),
                                            dbc.Col(
                                                [
                                                    dbc.Row(len(filtered_df), style={'font-size':'5rem'}),
                                                    dbc.Row('Total Enquiries', style={'font-size':'1.5rem'})
                                                ]
                                            , width={"size": 5, "offset": 1}),
                                        ], justify="around",
                                    ), style={'padding':'.5rem', 'background-color':'#92509f', 'color':'#FFF'}
                                ),
                                # dbc.CardFooter(
                                #     html.P("This card has an image at the top", className="card-text")
                                # ),
                            ],
                            
                        )
                    ], lg=6
                    ),

                    dbc.Col([
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.I(className="fa fa-user-shield fa-8x", **{'aria-hidden': 'true'}, children=None), 
                                                width={"size": 3}, align="center"
                                            ),
                                            dbc.Col(
                                                [
                                                    dbc.Row(filtered_df['conversion'].value_counts()['Converted'], style={'font-size':'5rem'}),
                                                    dbc.Row('Total Conversions', style={'font-size':'1.5rem'})
                                                ]
                                            , width={"size": 5, "offset": 1}),
                                        ], justify="around",
                                    ), style={'padding':'.5rem', 'background-color':'#d179e0', 'color':'#FFF'}
                                ),
                            ],
                            
                        )
                    ], lg=6
                    ),
               
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dbc.Col(
                                html.H4("Enquiry Summary Lead Wise"  , style={"margin-bottom": "0px !important"}, className='text-center'),
                            ),
                            dcc.Graph(
                                id='enquiry-lead-graph',
                                figure=enquiry_lead_figure,
                                style={'height': '90%'},
                                config={
                                    'displaylogo': False,
                                    # 'displayModeBar': True
                                }
                            )

                        ], style= {"margin-left": "20px", "margin-bottom": "20px", "margin-top": "20px" }
                        ),
                    ], lg=6),
                    dbc.Col([
                        html.Div([
                            dbc.Col(
                                html.H4("Enquiry Summary Month Wise"  , style={"margin-bottom": "0px !important"}, className='text-center'),
                            ),
                            dcc.Graph(
                                id='enquiry-month-graph',
                                figure=enq_month_fig,
                                style={'height': '90%'},
                                config={
                                    'displaylogo': False,
                                    # 'displayModeBar': True
                                }
                            )

                        ], style= {"margin-left": "20px", "margin-bottom": "20px", "margin-top": "20px" }
                        ),
                    ], lg=6),
           
                ])
            ], id="page-content")
        ])
    return layout





