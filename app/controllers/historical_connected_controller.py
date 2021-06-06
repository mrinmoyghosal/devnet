""" Historical data endpoints """
from flask import current_app
from flask_restx import Resource, Namespace, fields

from app.controllers.realtime_connected_controller import response
from app.services import DevNetApiService

api = Namespace(
    name='Historical Connected API',
    description='Check if developers are connected realtime',
    path='/'
)

response_with_registered = api.inherit(
    'HistoricalResponseWithRegistered', response, {
        'registered_at': fields.DateTime
    }
)

response_fields = api.model('HistoricalResponse', {
    'data': fields.List(
        fields.Nested(response_with_registered)
    ),
})


@api.route('/connected/register/<dev1>/<dev2>')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error',
    404: 'No data found',
    429: 'Rate Limit Exceeded',
    500: 'Internal Server Error',
})
class HistoricalConnectedController(Resource):
    """ This controller serves the GET endpoint which
    returns the historical data from realtime endpoints
    """

    @api.marshal_with(response_fields)
    def get(self, dev1: str, dev2: str):
        """ Return @HistoricalResponse swagger model """
        current_app.logger.info(
            f"Received register request for user {dev1}, {dev2}"
        )
        service = DevNetApiService(dev1, dev2)
        return {'data': service.get_all_historical_records()}
