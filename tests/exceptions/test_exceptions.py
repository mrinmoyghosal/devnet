from github import UnknownObjectException, RateLimitExceededException
from github.GithubException import BadCredentialsException
from tweepy import NotFound, TooManyRequests

from app.external_apis.tweepy_api import api as twitter_api
from app.services import TwitterFollowerService
from tests.utils import (
    mock_github_organisation_api_call,
    mock_github_api_call_throws,
    mock_twitter_followers_api_call,
)


def test_twitter_user_not_found_exception_handled_properly(client, mocker):
    list_of_orgs = {'dev1': ['abc', 'def'], 'dev2': ['xyc', 'mnmn']}
    mock_github_organisation_api_call(mocker, list_of_orgs)
    response = mocker.MagicMock()
    response.json.return_value = {'error': 'user not found'}
    mocker.patch.object(twitter_api, 'get_user', side_effect=NotFound(response))
    data = client.get('api/v1/connected/realtime/dev1/dev2')
    assert data.status_code == 404


def test_github_user_not_found_exception_handled_properly(client, mocker):
    mock_github_api_call_throws(mocker, UnknownObjectException('user not found', '', ''))
    data = client.get('api/v1/connected/realtime/dev1/dev2')
    assert data.status_code == 404


def test_github_rate_limit_exception_handled_properly_return_429(client, mocker):
    mock_github_api_call_throws(mocker, RateLimitExceededException('too many req', '', ''))
    data = client.get('api/v1/connected/realtime/dev1/dev2')
    assert data.status_code == 429


def test_github_other_exceptions_handled_properly_and_return_500(client, mocker):
    mock_github_api_call_throws(mocker, BadCredentialsException('bad credentials', '', ''))
    data = client.get('api/v1/connected/realtime/dev1/dev2')
    assert data.status_code == 500


def test_twitter_rate_limit_exception_handled_properly(client, mocker, mock_data):
    list_of_orgs = {'dev1': ['abc', 'def'], 'dev2': ['xyc', 'mnmn']}
    mock_github_organisation_api_call(mocker, list_of_orgs)
    mocker.patch.object(
        TwitterFollowerService,
        'get_user_ids',
        return_value=mock_data['twitter_user_id_with_match'],
    )
    response = mocker.MagicMock()
    response.json.return_value = {'error': 'user not found'}
    mock_twitter_followers_api_call(mocker, TooManyRequests(response))
    data = client.get('api/v1/connected/realtime/dev1/dev2')
    assert data.status_code == 429
