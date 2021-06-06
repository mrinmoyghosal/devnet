"""Flask configuration."""
from os import getenv


def get_required_env_var(name, default_val=None):
    val = getenv(name, default_val)
    if not val:
        print(f"Environment variable value is not present - {name}")
        exit(0)
    return val


class Config:
    """Set Flask config variables."""
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=C0103

    FLASK_ENV = 'development'
    TESTING = False
    SECRET_KEY = getenv('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:////tmp/devnetdb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # log level
    LOG_TYPE = getenv('LOG_TYPE', 'stream')
    LOG_LEVEL = getenv("LOG_LEVEL", "INFO")

    # Twitter Credentials
    CONSUMER_KEY = get_required_env_var(
        'TWITTER_CONSUMER_KEY',
        'some_consumer_key',
    )

    CONSUMER_SECRET = get_required_env_var(
        'TWITTER_CONSUMER_SECRET',
        'some_consumer_secret',
    )

    ACCESS_TOKEN = get_required_env_var(
        'TWITTER_ACCESS_TOKEN',
        'some_access_token_key',
    )

    ACCESS_TOKEN_SECRET = get_required_env_var(
        'TWITTER_ACCESS_TOKEN_SECRET',
        'some_access_token_key_secret',
    )

    # Github Access Token
    GITHUB_ACCESS_TOKEN = get_required_env_var(
        'GITHUB_ACCESS_TOKEN',
        'github_access_token',
    )

    def __init__(self):
        pass
