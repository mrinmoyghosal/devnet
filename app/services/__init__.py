""" DevNetApiService - main service entrypoint """
from datetime import datetime
from typing import List, Dict

import pandas as pd
from flask import current_app

from app.exceptions import NoRecordsFoundException
from app.external_apis.github_api import api as github_api
from app.external_apis.tweepy_api import api as tweepy_api
from app.models import db
from app.models.dev_net_entity import DeveloperConnectedData
from app.services.github_organisation_service import GithubOrganisationService
from app.services.twitter_follower_service import TwitterFollowerService

tw_svc = TwitterFollowerService(tweepy_api)
github_svc = GithubOrganisationService(github_api)


class DevNetApiService:
    """
    Devnet api service takes two username as parameter
    and it exposes a function `is_connected`
    that determines if both user follow each other and
    they share atleast one common organisation in github
    """

    dev1: str
    dev2: str

    def __init__(self, dev1: str, dev2: str):
        self.dev1, self.dev2 = dev1, dev2
        self.dev1, self.dev2 = self.sort_user_names()

    def is_connected(self) -> dict:
        """
        Check if two username follow each other in
        twitter and share at least one common github organisations
        :return: @DeveloperConnectedData object as dict
        """
        # Get both user's data
        both_devs = [self.dev1, self.dev2]

        current_app.logger.info(
            f"Retreiving github organisation data for users - {both_devs}"
        )
        org_df: pd.DataFrame = github_svc.get_org_df(both_devs)

        current_app.logger.info(
            f"Retreiving twitter userid  for users - {both_devs}"
        )
        tw_user_ids: Dict[str, str] = tw_svc.get_user_ids(both_devs)

        current_app.logger.info(
            f"Retreiving twitter follower ids data for users - {both_devs}"
        )
        followers_data: pd.DataFrame = tw_svc.get_followers_df(both_devs)

        # Check if they follow each other and share atleast one common org
        org_data_match: pd.Series = org_df[self.dev1].isin(org_df[self.dev2])
        is_share_same_orgs: bool = org_data_match.any()

        mutual_orgs: List[str] = []
        if is_share_same_orgs:
            mutual_orgs = org_df[org_data_match][self.dev1]
            mutual_orgs = mutual_orgs.dropna().values.tolist()

        current_app.logger.info(
            f"Users share organisations in github - "
            f"{is_share_same_orgs}, orgs - {mutual_orgs}"
        )

        # Find if user1 is followed by user2 or not -
        # false means they user2 follows user1
        dev1_is_not_followed_by_dev2 = followers_data[
            followers_data[self.dev1] == tw_user_ids[self.dev2]
        ].empty
        current_app.logger.info(
            f"{self.dev1} is not followed by "
            f"{self.dev2} - {dev1_is_not_followed_by_dev2}"
        )

        # Find if user2 is followed by user1 or not -
        # false means the user1 follows user2
        dev2_is_not_followed_by_dev1 = followers_data[
            followers_data[self.dev2] == tw_user_ids[self.dev1]
        ].empty
        current_app.logger.info(
            f"{self.dev2} is not followed by "
            f"{self.dev1} - {dev2_is_not_followed_by_dev1}"
        )

        # returns True if both are false (means they follow each other)
        is_follow_each_other = not any(
            [
                dev1_is_not_followed_by_dev2,
                dev2_is_not_followed_by_dev1
            ]
        )
        current_app.logger.info(
            f"{self.dev1} and {self.dev2} both "
            f"follows each other - {is_follow_each_other}"
        )

        # Finally decide if they are connected
        is_connected: bool = is_share_same_orgs & is_follow_each_other
        current_app.logger.info(
            f"{self.dev1} and {self.dev2} both "
            f"are fully connected - {is_connected}"
        )

        # initialize the sql-alchemy entity
        row = DeveloperConnectedData(
            registered_at=datetime.utcnow(),
            first_dev_name=self.dev1,
            second_dev_name=self.dev2,
            connected=is_connected,
            organisations=mutual_orgs if is_connected else []
        )
        db.session.add(row)
        db.session.commit()
        current_app.logger.info(
            f"{self.dev1} and {self.dev2} connection "
            f"data stored in db.."
        )
        return row.as_dict()

    def get_all_historical_records(self) -> List[dict]:
        """
        Get all historical records for the given username pair
        :return: a list of @DeveloperConnectedData object serialized as dict
        """
        filtered_res = DeveloperConnectedData.query.filter_by(
            first_dev_name=self.dev1,
            second_dev_name=self.dev2
        )
        if filtered_res.count() == 0:
            raise NoRecordsFoundException(
                f"No records found for this username pairs "
                f"- {self.dev1}, {self.dev2}"
            )

        all_rows = [
            item.as_dict() for item in
            filtered_res.all()
        ]
        return all_rows

    def sort_user_names(self) -> List[str]:
        """ Sort the usernames """
        return sorted([self.dev1, self.dev2])
