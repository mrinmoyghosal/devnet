import pandas as pd
from pytest_mock import MockerFixture

from app.services import DevNetApiService, GithubOrganisationService, TwitterFollowerService


def mock_patcher(mocker: MockerFixture, mock_data: dict, keys: dict):
    mocker.patch.object(
        GithubOrganisationService,
        'get_org_df',
        return_value=pd.DataFrame(mock_data[keys['organisation_data']]),
    )

    mocker.patch.object(
        TwitterFollowerService,
        'get_followers_df',
        return_value=pd.DataFrame(mock_data[keys['followers_data']]),
    )

    mocker.patch.object(
        TwitterFollowerService,
        'get_user_ids',
        return_value=mock_data[keys['twitter_user_ids']],
    )


def test_dev_net_api_service_sort_usernames_in_init():
    service = DevNetApiService("dev2", "dev1")
    assert service.dev1 == "dev1"
    assert service.dev2 == "dev2"


def test_dev_net_api_service_return_connected_true(session, mocker: MockerFixture, mock_data, app):
    mock_patcher(
        mocker,
        mock_data,
        {
            'organisation_data': 'connected_organisations',
            'followers_data': 'follower_ids',
            'twitter_user_ids': 'twitter_user_id_with_match'
        }
    )
    with app.app_context():
        service = DevNetApiService("dev2", "dev1")
        data = service.is_connected()
        assert data['connected']
        assert data['organisations'] == ["abc"]


def test_return_connected_false_when_users_dont_follow_each_other_in_twitter_but_share_orgs_in_github(
        session, mocker: MockerFixture, mock_data, app
):
    mock_patcher(
        mocker,
        mock_data,
        {
            'organisation_data': 'connected_organisations',
            'followers_data': 'follower_ids',
            'twitter_user_ids': 'twitter_user_id_without_match'
        }
    )
    with app.app_context():
        service = DevNetApiService("dev2", "dev1")
        data = service.is_connected()
        assert not data['connected']
        assert data['organisations'] == []


def test_return_connected_false_when_users_follow_each_other_in_twitter_but_no_shared_org_in_github(
        session, mocker: MockerFixture, mock_data, app
):
    mock_patcher(
        mocker,
        mock_data,
        {
            'organisation_data': 'disconnected_organisations',
            'followers_data': 'follower_ids',
            'twitter_user_ids': 'twitter_user_id_with_match'
        }
    )
    with app.app_context():
        service = DevNetApiService("dev2", "dev1")
        data = service.is_connected()
        assert not data['connected']
        assert data['organisations'] == []


def test_return_connected_false_when_users_follow_each_other_in_twitter_but_no_shared_org_in_github(
        session, mocker: MockerFixture, mock_data, app
):
    mock_patcher(
        mocker,
        mock_data,
        {
            'organisation_data': 'disconnected_organisations',
            'followers_data': 'follower_ids',
            'twitter_user_ids': 'twitter_user_id_with_match'
        }
    )
    with app.app_context():
        service = DevNetApiService("dev2", "dev1")
        data = service.is_connected()
        assert not data['connected']
        assert data['organisations'] == []


def test_return_connected_false_when_only_one_user_follow_other_in_twitter(
        session, mocker: MockerFixture, mock_data, app
):
    mock_patcher(
        mocker,
        mock_data,
        {
            'organisation_data': 'disconnected_organisations',
            'followers_data': 'follower_ids',
            'twitter_user_ids': 'twitter_user_id_with_match_one_user'
        }
    )
    with app.app_context():
        service = DevNetApiService("dev2", "dev1")
        data = service.is_connected()
        assert not data['connected']
        assert data['organisations'] == []
