from datetime import datetime

from flask import Response

from app.models.dev_net_entity import DeveloperConnectedData


def test_historical_connected_controller_return_whatever_it_found_in_db_for_given_usernames(session, client):
    # prepare the entity data
    dev1_dev2_data = [
        {
            'registered_at': datetime.utcnow(),
            'first_dev_name': 'dev1',
            'second_dev_name': 'dev2',
            'connected': True,
            'organisations': ['def', 'def']
        },
        {
            'registered_at': datetime.utcnow(),
            'first_dev_name': 'dev1',
            'second_dev_name': 'dev2',
            'connected': True,
            'organisations': ['xyz', 'def', 'def']
        }
    ]

    # add all entities
    session.add_all([DeveloperConnectedData(**data) for data in dev1_dev2_data])
    session.commit()
    # get the response back from api
    res: Response = client.get('/api/v1/connected/register/dev1/dev2')
    json_data = res.get_json()
    assert res.status_code == 200
    assert len(json_data['data']) == 2

    # prepare the expected output
    dev1_dev2_data_response = [
        dict(i, registered_at=i['registered_at'].isoformat())
        for i in dev1_dev2_data
    ]

    for i in range(len(json_data['data'])):
        is_all_true = all(
            [
                json_data['data'][i][key] == dev1_dev2_data_response[i][key]
                for key in json_data['data'][i].keys()
            ]
        )
        assert is_all_true


def test_historical_connected_controller_return_404_if_no_entry_is_found(session, client):
    res: Response = client.get('/api/v1/connected/register/dev1/dev2')
    json_data = res.get_json()
    assert res.status_code == 404
    assert json_data == {'errors': ['No records found for this username pairs - dev1, dev2']}
