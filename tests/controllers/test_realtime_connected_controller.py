from flask import Response
from pytest_mock import MockerFixture

from app.services import DevNetApiService


def test_realtime_connected_controller_return_connected_true_and_organisations(client, mocker: MockerFixture):
    return_data = {
        'connected': True,
        'organisations': ["blach", "starlink"]
    }
    mocker.patch.object(DevNetApiService, 'is_connected', return_value=return_data)
    res: Response = client.get('/api/v1/connected/realtime/dev1/dev2')
    json_data = res.get_json()
    assert res.status_code == 200
    assert json_data == return_data


def test_realtime_connected_controller_return_connected_false_and_organisations(client, mocker: MockerFixture):
    return_data = {
        'connected': False,
        'organisations': []
    }
    mocker.patch.object(DevNetApiService, 'is_connected', return_value=return_data)
    res: Response = client.get('/api/v1/connected/realtime/dev1/dev2')
    json_data = res.get_json()
    assert res.status_code == 200
    assert json_data == return_data
