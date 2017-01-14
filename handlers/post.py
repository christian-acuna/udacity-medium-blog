from models.post import Post
from handlers.handler import Handler
from google.appengine.ext import db

class PostHandler(Handler):
    """Class that handels the rendering of a single post"""
    def render_post(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if not post:
            self.error(404)
            return self.render("404.html")

        # post = Post.get_by_id(int(post_id))

        self.render("post.html", post = post)

    def get(self, post_id):
        self.render_post(post_id)
