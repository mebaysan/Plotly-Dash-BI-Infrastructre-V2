"""
    Creating a core app (server)
    Database and login processes are configured in this file
"""
# Dash app initialization
import dash

# User management initialization
import os
from login import login_manager

# from users_mgt import db
from models.user import UserModel

# Database initialization
from db import db

# Flask import to handle URL issues
from flask import redirect
import flask

# Dash Bootstrap
import dash_bootstrap_components as dbc

# get .env variables
from dotenv import load_dotenv

# to set session life time
from datetime import timedelta

# mail
from mail import mail
from distutils.util import strtobool

# migration
from flask_migrate import Migrate

load_dotenv()

server = flask.Flask(__name__)


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    server=server,
)
app.title = "Dash App Management Dashboard"


app.permanent_session_lifetime = timedelta(minutes=20)

# config (server [Flask])
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=os.environ["DB_URL"],
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    MAIL_SERVER=os.environ["MAIL_SERVER"],
    MAIL_PORT=os.environ["MAIL_PORT"],
    MAIL_USERNAME=os.environ["MAIL_USERNAME"],
    MAIL_PASSWORD=os.environ["MAIL_PASSWORD"],
    MAIL_USE_TLS=bool(strtobool(os.environ["MAIL_USE_TLS"])),
    MAIL_USE_SSL=bool(strtobool(os.environ["MAIL_USE_SSL"])),
    MAIL_DEBUG=server.debug,
)

# set up database for the server
db.init_app(server)
migrate = Migrate(server, db)  # flask-migration

# set up the LoginManager for the server
login_manager.init_app(server)
login_manager.login_view = "/login"

# set up the flask mail for the server
mail.init_app(server)


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect("/login/")


@server.before_first_request
def create_tables():
    db.create_all()
