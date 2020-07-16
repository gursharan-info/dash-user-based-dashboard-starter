import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask, os
from flask import Flask
# from flask_caching import Cache
from dotenv import load_dotenv

# Initiate Flask 
server = flask.Flask(__name__)

# Wrap Dash with Flask application
app = dash.Dash(
		__name__,
    	server=server,
		meta_tags=[
			{"name": "viewport", "content": "width=device-width, initial-scale=1"},
			{"name": "robots", "content": "noindex"},
			{"name": "googlebot", "content": "noindex"}
		],
	)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.title="APP Title"
app.config.suppress_callback_exceptions = True

# Get the envionment VARS from .env file which enable the application to use "flask run" instead of old "python <filename>.py" metthod
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
environment_configuration = os.getenv('FLASK_ENV')
# print(environment_configuration)

if environment_configuration == "development":
    # Use configuration for development environment. eg Database connection via SqlAlchemy
	pass
else:
    # Use configuration for production environment
	pass
