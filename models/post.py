"""This is the Post model module"""
from google.appengine.ext import db

from models.comment import Comment

class Post(db.Model):
    """Class for blog post"""
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.StringProperty(required = True)
    likes = db.IntegerProperty()
    liked_by = db.StringListProperty()
    author_id = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def get_comments(self):
        """function to display all comments for each post"""
        q = db.Query(Comment)
        self.comments = q.ancestor(self).order('created')
        self.comment_count = q.ancestor(self).order('created').count()
        return self.comments
