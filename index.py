import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app, server
from apps import home_dashboard, business_reporting
from common import common_functions, constants
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

private_key = constants.private_key.encode()
f = Fernet(private_key)


content = html.Div(id="page-container")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Spinner(html.Div(id="root-loader"),color="success", spinner_style=constants.SPINNER_CLASS),
    content
])

pages = ["dashboard","business-reporting"]

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"{page}-link", "active") for page in pages],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False
    return [pathname == f"/{page}" for page in pages]


# this function is used to toggle the is_open property of each Collapse
@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    elif n and classname == "collapsed":
        return ""
    else:
        return "collapsed"


@app.callback(
    [
        Output('page-container', 'children'),
        Output("root-loader", "children"),
    ],
    [
        Input('url', 'pathname'),
        Input('url', 'search')  
    ]
)   
def display_page(pathname, search):
    
    args = common_functions.get_args(search)
    public_key = common_functions.get_public_key(search)

    if public_key:
        encrypted_public_key= public_key[0].encode()
        try:
            decrypted_public_key = f.decrypt(encrypted_public_key)
            # print(decrypted_public_key)

            if pathname == '/':
                return home_dashboard.get_layout(args,search), ""
            elif pathname == '/dashboard':
                return home_dashboard.get_layout(args,search), "" 
            elif pathname == '/business-reporting':
                return business_reporting.get_layout(args,search), ""              
            else:
                return html.Div([
                        common_functions.get_menu(args,search),
                        dbc.Jumbotron(
                            [
                                html.H1("404: Not found", className="text-danger"),
                                html.Hr(),
                                html.P(f"The url, {pathname} was not recognised..."),
                            ], id="page-content"
                        )
                ]), ""
        except:
            # print('Incorrect public key.')
            return html.Div([
                    dbc.Jumbotron(
                        [
                            html.H1("Restricted Access", className="text-danger"),
                            html.Hr(),
                            html.H4("Incorrect Token", className="text-danger"),
                            html.P(f"Your account is not allowed to view this page."),
                        ], id="page-content", className="restriction-box"
                    )
                ]), ""
    else:
        return html.Div([
                dbc.Jumbotron(
                    [
                        html.H1("Restricted Access", className="text-danger"),
                        html.Hr(),
                        html.H4("No Token provided", className="text-danger"),
                        html.P(f"Your account is not allowed to view this page."),
                    ], id="page-content", className="restriction-box"
                )
            ]), ""


if __name__ == "__main__":
    app.run_server(port=8005,debug=True)
    print ('################### Restarting @ ###################')
