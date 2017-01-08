import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class NewPost(Handler):
    def render_front(self, subject="", content="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")

        self.render("new_post.html", subject=subject, content=content, error=error, posts = posts)

    def get(self):
        self.render_front()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if title and art:
            a = Post(subject = title, contest = art)
            a.put() #store in database
            self.redirect('/blog')

        else:
            error = 'we need both a subject line and some content!'
            self.render_front(subject, content, error)


class MainPage(Handler):
    def render_front(self, subject="", content="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")

        self.render("front.html", subject=subject, content=content, error=error, posts = posts)

    def get(self):
        self.render_front()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if title and art:
            a = Post(subject = title, contest = art)
            a.put() #store in database
            self.redirect('/blog')

        else:
            error = 'we need both a subject line and some content!'
            self.render_front(subject, content, error)

app = webapp2.WSGIApplication([('/blog', MainPage), ('/blog/newpost', NewPost)], debug=True)
