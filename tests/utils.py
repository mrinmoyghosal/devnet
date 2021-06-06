from app.external_apis.github_api  import api as github_api
from app.services.twitter_follower_service import TwitterFollowerService


def mock_github_organisation_api_call(mocker, return_orgs):
    all_mocks = []
    for user, orgs in return_orgs.items():
        mock = mocker.MagicMock()
        org_mocks_per_user = []
        for org in orgs:
            org_mock = mocker.PropertyMock()
            org_mock.name = org
            org_mocks_per_user.append(org_mock)

        mock.get_orgs.return_value = org_mocks_per_user
        all_mocks.append(mock)
    mocker.patch.object(github_api, 'get_user', side_effect=all_mocks)


def mock_github_api_call_throws(mocker, exception):
    mocker.patch.object(github_api, 'get_user', side_effect=exception)


def mock_twitter_followers_api_call(mocker, data):
    mocker.patch.object(TwitterFollowerService, 'get_follower_ids', side_effect=data)