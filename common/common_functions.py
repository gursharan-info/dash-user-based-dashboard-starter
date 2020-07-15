import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import sqlalchemy.interfaces
import time, json, os
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine
import numpy as np
from shapely.geometry import LineString, MultiLineString
from urllib.parse import parse_qs
from common import constants as const
from config import DATABASE_URI
from sqlalchemy.orm import sessionmaker
from flask import request


def get_public_key(search):
    
    params = parse_qs(search[1:]) if search else None
    if params:
        if 'public_key' in search:
            return params['public_key']
        else:
            return None
    else:
        return None

def get_args(search):

    params = parse_qs(search[1:]) if search else None
    if params:
        if 'user_id' in search:
            user_id = params['user_id'][0]
            is_admin = None
        else:
            user_id = None
            is_admin = True
        types = [ 
            {'type': 'user_id', 'value': user_id},
            {'type': 'is_admin', 'value': is_admin},
        ]
        args = [arg for arg in types if arg['value'] is not None]
    else:
        args = None

    return args


''' Wrapper function to measure execution timing when required 
    Use this as a decorator before any function to use, eg: @timing
'''
def timing(f):
    def wrap(*args):
        time1 = time.time() 
        ret = f(*args)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap



def get_menu(args, search):
    
    # print("search",search)
    search = search if search else ''
    is_admin = False if search else True

    if args:
        isChain = True if args[0]['type'] == 'ChainId' else False
    else:
        isChain = False
    
    # print('isChain=',isChain)

    sidebar_header = dbc.Row(
        [
            dbc.Col(html.H2("APP Title", className="display-4")),
            dbc.Col(
                [
                    html.Button(
                        # use the Bootstrap navbar-toggler classes to style
                        html.Span(className="navbar-toggler-icon"),
                        className="navbar-toggler",
                        # the navbar-toggler classes don't set color
                        style={
                            "color": "rgba(0,0,0,.5)",
                            "borderColor": "rgba(0,0,0,.1)",
                        },
                        id="navbar-toggle",
                    ),
                    html.Button(
                        # use the Bootstrap navbar-toggler classes to style
                        html.Span(className="navbar-toggler-icon"),
                        className="navbar-toggler",
                        # the navbar-toggler classes don't set color
                        style={
                            "color": "rgba(0,0,0,.5)",
                            "borderColor": "rgba(0,0,0,.1)",
                        },
                        id="sidebar-toggle",
                    ),  
                ],
                # the column containing the toggle will be only as wide as the
                # toggle, resulting in the toggle being right aligned
                width="auto",
                # vertically align the toggle in the center
                align="center",
            ),
        ]
    )
    sidebar = html.Div(
        [
            sidebar_header,
            html.Div(
                [
                    html.Hr(),
                ],
                id="blurb"
            ),
            dbc.Collapse(
                dbc.Nav([
                        
                        dbc.NavLink("Dashboard", href=f"/dashboard{search}", id="dashboard-link"),

                        dbc.NavLink("Business Reporting", href=f"/business-reporting{search}", id="business-reporting-link"),

                    ],
                    vertical=True,
                    pills=True
                ),
                id="collapse",
            ),
        ],
        id="sidebar", 
        # className="collapsed"
    )

    return sidebar    

