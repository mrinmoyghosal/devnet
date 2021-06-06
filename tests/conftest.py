import os

import pytest

from app import init_app
from app.models import db as _db

TESTDB = '/tmp/test.db'
TEST_DATABASE_URI = f'sqlite:///{TESTDB}'


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI
    }
    app = init_app()
    app.config.update(settings_override)
    return app


@pytest.fixture(scope='session')
def client(app):
    with app.test_client() as client:
        return client


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TESTDB):
        os.unlink(TESTDB)

    def teardown():
        _db.drop_all()
        os.unlink(TESTDB)

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture()
def mock_data():
    return {
        'connected_organisations' : {
            'dev1': ['abc', 'deg'],
            'dev2': ['xyz', 'abc']
        },
        'disconnected_organisations': {
            'dev1': ['abc', 'deg'],
            'dev2': ['xyz', 'njh']
        },
        'follower_ids': {
            'dev1': ['123', '456'],
            'dev2': ['877', '090']
        },
        'twitter_user_id_with_match': {
            'dev1': '877',
            'dev2': '123'
        },
        'twitter_user_id_without_match': {
            'dev1': '988',
            'dev2': '787'
        },
        'twitter_user_id_with_match_one_user': {
            'dev1': '988',
            'dev2': '123'
        }
    }
