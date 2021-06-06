""" SQLAlchemy entity to store the response """
from datetime import datetime

from app.models import db, JsonEncodedList


class DeveloperConnectedData(db.Model):
    """
    Developer connected data entity represents each row entry in the table
    """
    id = db.Column(db.Integer, primary_key=True)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow())
    first_dev_name = db.Column(db.String, nullable=False)
    second_dev_name = db.Column(db.String, nullable=False)
    connected = db.Column(db.Boolean, nullable=False)
    organisations = db.Column(JsonEncodedList, nullable=True)

    def as_dict(self) -> dict:
        """
        Return the row as dict
        :return: dict containing column name as key and it's value
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'<DeveloperConnectedData between ' \
               f'{self.first_dev_name} <-> {self.second_dev_name} >'
