""" SQLAlchemy Initializer """
import json

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext import mutable

# Initialize the ORM
db = SQLAlchemy()
migrate = Migrate()


# Hack - For postgres we can directly use json/jsonb type
# Model Extension for storing array of string as json in sqlite
# pylint: disable=C0116
class JsonEncodedList(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""

    impl = db.Text

    @property
    def python_type(self):
        pass

    def process_literal_param(self, value, dialect):
        pass

    def process_bind_param(self, value, dialect):
        if value is None:
            return '[]'
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        return json.loads(value)


mutable.MutableList.associate_with(JsonEncodedList)
