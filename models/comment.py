"""This module is for the Comments model"""

from google.appengine.ext import db

class Comment(db.Model):
    """Class for Comments model"""
    body = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    author_id = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @classmethod
    def write_entity(cls, body, author, parent_key, author_id):
        return cls(body = body,
                   author = author,
                   parent = parent_key,
                   author_id = author_id)
