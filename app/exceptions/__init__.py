"""Exception classes"""


class TwitterRateLimitException(Exception):
    """ This exception is thrown when twitter returns 429 -
    Rate limit exceeded response"""


class TwitterUserNotFoundException(Exception):
    """ This exception is thrown when the supplied user is not
    found in twitter
    """


class GithubUserNotFoundException(Exception):
    """ This exception is thrown when the supplied user is not
        found in github
        """


class GithubRateLimitException(Exception):
    """ This exception is thrown when github returns 429 -
        Rate limit exceeded response"""


class GithubServiceException(Exception):
    """ Generic Github service exception is thrown when the exception
        from github is not in the above exceptions"""


class TwitterServiceException(Exception):
    """ Generic twitter service exception is thrown when the exception
    from twitter is not in the above exceptions"""


class NoRecordsFoundException(Exception):
    """ This exception is thrown when no records found for the given
    username pairs"""
