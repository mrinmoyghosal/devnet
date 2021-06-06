""" Github API"""
from github import Github

from config import Config

# create the github api
api = Github(Config.GITHUB_ACCESS_TOKEN)
