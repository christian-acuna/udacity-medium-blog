from handlers.handler import Handler
from google.appengine.ext import db
from models.post import Post

class WelcomeHandler(Handler):
    def get(self):
        # self.user is set in initialize function in Handler
        if self.user:
            q = db.Query(Post)
            posts = q.filter('author_id =', self.user.key().id())
            self.render('welcome.html', username = self.user.username, posts = posts)
        else:
            self.redirect('/signup')
