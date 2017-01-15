"""This is the Post model module"""
from google.appengine.ext import db

class Post(db.Model):
    """Class for blog post"""
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.StringProperty(required = True)
    likes = db.IntegerProperty()
    likers = db.StringListProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
