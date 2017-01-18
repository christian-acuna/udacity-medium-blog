from models.post import Post
from handlers.handler import Handler
from google.appengine.ext import db

class PostHandler(Handler):
    """Class that handels the rendering of a single post"""
    def render_post(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if not post:
            return self.redirect("/blog?error=2")

        comments = post.get_comments()
        self.render("posts/post.html", post = post, comments = comments)

    def get(self, post_id):
        self.render_post(post_id)
