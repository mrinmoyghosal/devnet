""" API v1 routes """
from flask import Blueprint
from flask_restx import Api

from app.controllers.historical_connected_controller import (
    api as historical_api
)
from app.controllers.realtime_connected_controller import (
   api as realtime_api
)

devnetapi = Blueprint("DeveloperConnectedApi", __name__)

api = Api(
    devnetapi,
    version='1.0',
    title='DeveloperConnectedApi',
    description='A DeveloperConnectedApi',
    doc='/'
)

api.add_namespace(realtime_api)
api.add_namespace(historical_api)
