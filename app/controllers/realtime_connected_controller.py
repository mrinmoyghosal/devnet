""" Realtime Developer Connected API Controller """
import logging

from flask import current_app
from flask_restx import Resource, Namespace, fields

from app.services import DevNetApiService

api = Namespace(
    name='Realtime Connected API',
    description='Check if developers are connected realtime',
    path='/'
)
api.logger.setLevel(logging.INFO)

response = api.model('RealtimeResponse', {
    'connected': fields.Boolean(default=False),
    'organisations': fields.List(fields.String)
})


@api.route('/connected/realtime/<dev1>/<dev2>')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error',
    404: 'No data found',
    429: 'Rate Limit Exceeded',
    500: 'Internal Server Error',
})
class RealtimeConnectedController(Resource):
    """
    Realtime Connected API Controller
    """
    @api.marshal_with(response)
    def get(self, dev1: str, dev2: str):
        """
        Receives two path variable - dev1, dev2 and returns if they are
        connected in twitter and github
        :param dev1: String username of developer1
        :param dev2: String username of developer2
        :return: return @RealtimeResponse swagger model
        """
        current_app.logger.info(
            f"Received realtime request for user {dev1}, {dev2}"
        )
        service = DevNetApiService(dev1, dev2)
        data = service.is_connected()
        return data
