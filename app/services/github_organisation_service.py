"""" Github service that fetches users organisations info """
from typing import Generator

import pandas as pd
from github import (
    Github,
    GithubException,
    UnknownObjectException,
    RateLimitExceededException,
)

from app.exceptions import (
    GithubServiceException,
    GithubUserNotFoundException,
    GithubRateLimitException,
)


class GithubOrganisationService:
    """
    Github service takes a @Github api object as parameter for initialization.
    It exposes one functions to retrive users organisations data from github
    """

    api: Github

    def __init__(self, api: Github):
        self.api = api

    def get_organisations_by_username(
            self, username,
    ) -> Generator[str, None, None]:
        """ Get a list of organisations for a given user """
        return (
            org.name
            for org in self.api.get_user(login=username).get_orgs()
        )

    def get_org_df(
            self, usernames,
    ) -> pd.DataFrame:
        """ Returns a pd.DataFrame object where each column
            heading is a username from the usernames
            list and it contains all the organisations name in the rows
        """
        try:
            data = pd.DataFrame({
                username: pd.Series(
                    self.get_organisations_by_username(username)
                ) for username in usernames
            })
            return data
        except UnknownObjectException as error:
            raise GithubUserNotFoundException(
                f"Github user not found for these names-"
                f"{usernames}, github response - {error.data}"
            )
        except RateLimitExceededException as error:
            raise GithubRateLimitException(
                f"Github rate limit exceeded, "
                f"github response - {error.data}"
            )
        except GithubException as error:
            raise GithubServiceException(
                f"Exception occurred during getting organisations of "
                f"these two developers - {usernames}, "
                f"github response - {error.data} "
            )
