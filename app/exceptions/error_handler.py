""" Global Exception Handler """
from flask import Blueprint, jsonify

from app.exceptions import (
    TwitterServiceException,
    GithubServiceException,
    GithubUserNotFoundException,
    TwitterUserNotFoundException,
    TwitterRateLimitException,
    GithubRateLimitException, NoRecordsFoundException,
)

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(GithubServiceException)
@errors.app_errorhandler(TwitterServiceException)
def handle_error(error: Exception, status_code: int = 500):
    """
    Handle general exceptions raised from Twitter and Github
    :param error: Exception caught in the process
    :param status_code: status code - default 500
    :return: json result containing exception message and status code
    """
    response = {
        'errors': [str(error)]
    }
    return jsonify(response), status_code


@errors.app_errorhandler(GithubUserNotFoundException)
@errors.app_errorhandler(TwitterUserNotFoundException)
@errors.app_errorhandler(NoRecordsFoundException)
def handle_404_errors(error: Exception):
    """
    Handle 404 exceptions raised from Twitter and Github
    :param error: Exception caught in the process
    :return: json result containing exception message and status code
    """
    return handle_error(error, 404)


@errors.app_errorhandler(TwitterRateLimitException)
@errors.app_errorhandler(GithubRateLimitException)
def handle_429_errors(error: Exception):
    """
    Handle rate limit exceptions raised from Twitter and Github
    :param error: Exception caught in the process
    :return: json result containing exception message and status code
    """
    return handle_error(error, 429)
