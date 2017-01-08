import os
import webapp2
import jinja2
import re
import hashlib
import hmac
from google.appengine.ext import db

SECRET = 'imsosecret'
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

# def blog_key(name = 'default'):
#     return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)




class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class HomeHandler(Handler):
    def get(self):
        self.render("home.html")

class MainPage(Handler):
    def render_front(self, visits):
        posts = Post.all().order('-created')
        self.render("front.html", posts = posts, visits = visits)

    def get(self):
        visits = 0
        visits_cookie_val = self.request.cookies.get('visits')
        if visits_cookie_val:
            cookie_val = check_secure_val(visits_cookie_val)
            if cookie_val:
                visits = int(cookie_val)

        visits += 1
        new_cookie_val = make_secure_val(str(visits))
        self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)
        self.render_front(visits)

class NewPost(Handler):
    def render_form(self, subject="", content="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")

        self.render("new_post.html", subject=subject, content=content, error=error, posts = posts)

    def get(self):
        self.render_form()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            a = Post(subject = subject, content = content)
            a.put() #store in database
            id = a.key().id()
            self.redirect('/blog/' + str(id) )
        else:
            error = 'A post needs both a subject line and content'
            self.render_form(subject=subject, content=content, error=error)


class PostHandler(Handler):
    def render_post(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if not post:
            self.error(404)
            return

        # post = Post.get_by_id(int(post_id))
        self.render("post.html", post = post)

    def get(self, post_id):
        self.render_post(post_id)
class LoginHandler(Handler):
    def get(self):
        self.render("login.html")



app = webapp2.WSGIApplication([('/', HomeHandler),
                              ('/blog/?', MainPage),
                              ('/blog/newpost', NewPost),
                              (r'/blog/(\d+)', PostHandler),
                              ('/login', LoginHandler)], debug=True)
