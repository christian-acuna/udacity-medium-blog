import os
import webapp2
import random
from string import letters
import jinja2
import re
import hashlib
import hmac
from google.appengine.ext import db
import datetime
import json

from models.user import User

SECRET = '8389c4927f7bbdbf7385da1072b7d01b3bd59be32a1e038b'


template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        # calls global render_str with user as key in params so it is
        # available in each template
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = self.make_secure_val(val)
        # set cookie on Path to make sure cookies don't get set on
        # different paths
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and self.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    # sets the cookie to nothing
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    # called by the app engine framework
    # every request calls this function
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

    def check_secure_val(self, h):
        val = h.split('|')[0]
        if h == self.make_secure_val(val):
            return val

    def hash_str(self, s):
        return hmac.new(SECRET, s).hexdigest()

    def make_secure_val(self, s):
        return "%s|%s" % (s, self.hash_str(s))
