from models.user import User
from models.post import Post
from handlers.handler import Handler

class MainPage(Handler):
    """Class that handles showing all the blog posts on the /blog route"""
    def render_front(self, visits):
        posts = Post.all().order('-created')

        self.render("posts.html", posts = posts)

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