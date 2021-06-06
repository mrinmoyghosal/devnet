from pytest_mock import MockerFixture

from app.external_apis.github_api import api as github_api
from app.services import GithubOrganisationService
from tests.utils import mock_github_organisation_api_call


def test_github_organisation_service_return_all_organisations_name(mocker: MockerFixture):
    list_of_orgs = {'dev1': ['abc', 'def'], 'dev2': ['xyc', 'mnmn']}
    mock_github_organisation_api_call(mocker, return_orgs=list_of_orgs)
    data = list(GithubOrganisationService(github_api).get_organisations_by_username('dev1'))
    assert data == ['abc', 'def']


def test_github_organisation_service_return_all_organisations(mocker: MockerFixture):
    list_of_orgs = {'dev1': ['abc', 'def'], 'dev2': ['xyc', 'mnmn']}
    mock_github_organisation_api_call(mocker, return_orgs=list_of_orgs)
    data = GithubOrganisationService(github_api).get_org_df(['dev1', 'dev2'])
    actual_data = {'dev1': data['dev1'].tolist(), 'dev2': data['dev2'].tolist()}
    assert actual_data == list_of_orgs
