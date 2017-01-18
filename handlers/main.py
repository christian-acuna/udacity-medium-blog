from models.user import User
from models.post import Post
from handlers.handler import Handler

class MainPage(Handler):
    """Class that handles showing all the blog posts on the /blog route"""
    def render_front(self, visits):
        posts = Post.all().order('-created')
        error = self.request.get('error')
        message = self.request.get('msg')

        if error == '1':
            error = "You can only delete your own posts."
        elif error == '2':
            error = "No post found that matches that post identifier."

        if message == '1':
            message = "Your post has been successfully deleted"

        self.render("posts/posts.html", posts = posts, message = message, error = error)

    def get(self):
        visits = 0
        visits_cookie_val = self.request.cookies.get('visits')
        if visits_cookie_val:
            cookie_val = self.check_secure_val(visits_cookie_val)
            if cookie_val:
                visits = int(cookie_val)

        visits += 1
        new_cookie_val = self.make_secure_val(str(visits))
        self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)
        self.render_front(visits)
