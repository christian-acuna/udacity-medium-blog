from handlers.handler import Handler
from google.appengine.ext import db
from models.post import Post
from models.comment import Comment

class WelcomeHandler(Handler):
    def get(self):
        message = self.request.get('msg')
        if message == '1':
            message = "Your post has been successfully deleted"
        # self.user is set in initialize function in Handler
        if self.user:
            q_posts = db.Query(Post)
            posts = q_posts.filter('author_id =', self.user.key().id())
            q_comments = db.Query(Comment)
            comments = q_comments.filter('author_id =', self.user.key().id())
            self.render('welcome.html', username = self.user.username,
                                        posts = posts,
                                        comments = comments,
                                        message = message)
        else:
            self.redirect('/signup')
