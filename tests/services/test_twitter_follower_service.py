from app.external_apis.tweepy_api import api as twitter_api
from app.services import TwitterFollowerService
from tests.utils import mock_twitter_followers_api_call


def test_twitter_follower_service_returns_all_followers(mocker):
    data = [
        ['12345', '676767'],
        ['12356645', '9989893']
    ]
    mock_twitter_followers_api_call(mocker, data)
    service = TwitterFollowerService(twitter_api)
    response = service.get_followers_df(['dev1', 'dev2'])
    assert response['dev1'].tolist() == data[0]
    assert response['dev2'].tolist() == data[1]
