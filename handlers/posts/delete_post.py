from models.post import Post
from handlers.handler import Handler
from google.appengine.ext import db

class DeletePostHandler(Handler):
    """Class that deletes a post"""
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if not post:
            return self.redirect('/blog?error=2')

        if self.user and self.user.key().id() == post.author_id:
            db.delete(post.get_comments())
            post.delete()
            self.redirect('/welcome?msg=1')
        elif self.user:
            self.redirect('/blog?error=1')
        else:
            error = "You need to be logged in to delete a post!"
            return self.render('sessions/login.html', error = error)
