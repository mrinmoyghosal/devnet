"""This script contains the function that creates the flask app"""
from flask import Flask

from app.exceptions.error_handler import errors
from app.flask_log import LogSetup
from app.models import db, migrate
from app.routes_v1 import devnetapi


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # setup logger
    logs = LogSetup()
    logs.init_app(app)

    # Setup SqlAlchemy and flask-migrate
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # add v1 api endpoints
        app.register_blueprint(devnetapi, url_prefix='/api/v1/')
        # add error handler
        app.register_blueprint(errors)
        return app
