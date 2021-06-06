""" Twitter service that returns a list of followers for given usernames"""
from typing import List, Generator, Dict

import pandas as pd
from tweepy import API, Cursor, TweepyException, NotFound, TooManyRequests

from app.exceptions import (
    TwitterServiceException,
    TwitterRateLimitException,
    TwitterUserNotFoundException,
)


class TwitterFollowerService:
    """
    Twitter service needs a @tweepy.API object for initialization.
    It exposes functions to retrieve user's follower ids
    """
    def __init__(self, api: API):
        self.api = api

    def get_follower_ids(
            self,
            username: str,
    ) -> Generator[str, None, None]:
        """ Get list of follower ids for a given user"""
        return (
            ids for ids in
            Cursor(
                self.api.get_follower_ids,
                screen_name=username,
                stringify_ids=True
            ).items()
        )

    def get_user_ids(
            self,
            usernames: List[str]
    ) -> Dict[str, str]:
        """
        Takes a list of usernames and return twitter string ids
        :param usernames: list of usernames
        :return: dict containing username and id
        """
        try:
            return {
                user: self.api.get_user(
                    screen_name=user,
                    include_entities=False
                ).id_str
                for user in usernames
            }
        except NotFound as error:
            raise TwitterUserNotFoundException(
                f"Twitter user not found for these "
                f" usernames - {usernames},"
                f" twitter response - {str(error)}"
            )

    def get_followers_df(
            self,
            usernames: List[str],
    ) -> pd.DataFrame:
        """
        Return a pd.DataFrame object containing columns as
        username and rows as their list of follower ids
        :param usernames: list of username
        :return: pd.DataFrame containing user's follower ids
        """
        try:
            data = pd.DataFrame({
                user: pd.Series(
                    self.get_follower_ids(user)
                )
                for user in usernames
            })
            return data
        except NotFound as error:
            raise TwitterUserNotFoundException(
                f"Twitter user not found for these usernames - {usernames},"
                f" twitter response - {str(error)}"
            )
        except TooManyRequests as error:
            raise TwitterRateLimitException(
                f"Twitter rate limit exceeded, twitter response - {str(error)}"
            )
        except TweepyException as error:
            raise TwitterServiceException(
                f"Exception occurred during fetching followers of "
                f"these two user {usernames}, twitter response - {str(error)}"
            )
