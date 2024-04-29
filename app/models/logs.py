"""Defines the users object and provides functions to get and manipulate one"""

from datetime import datetime
import json

from app.databases import db

# pylint: disable=too-few-public-methods
class LogModel(db.Model):
    """Stores all logs from api calls"""

    __tablename__ = "logs"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    request_body = db.Column(db.String(200))
    response_code = db.Column(db.Integer(), nullable=False)
    error_response_body = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    def to_json(self):
        """Return json from log object"""

        json_thread = {
            'id': self.id,
            'userId': self.user_id,
            'url': self.url,
            'requestBody': None if self.request_body is None else json.loads(self.request_body),
            'responseCode': self.response_code,
            'errorResponseBody': None if self.error_response_body is None else json.loads(self.error_response_body),
            'createdAt': self.created_at,
        }
        return json_thread
