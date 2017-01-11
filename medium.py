import os
import webapp2
import random
from string import letters
import jinja2
import re
import hashlib
import hmac
from google.appengine.ext import db

#######################
####### Cookies #########
#######################
SECRET = '8389c4927f7bbdbf7385da1072b7d01b3bd59be32a1e038b'
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

################################
####### Template Setup #########
################################

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

# def blog_key(name = 'default'):
#     return db.Key.from_path('blogs', name)

#######################
####### Post #########
#######################
#######################
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

#######################
####### USER #########
#######################

# make a string of 5 letters
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))
# makes a password hash. Takes a username and pw (with optinal param for salt)
# return salt, hashed version of (name + pw + salt)
# store this in the database
def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s,%s" % (salt, h)

# function to verify password
# makes sure hash from database matches the new hash based on params
def vald_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

class User(db.Model):
    username = db.StringProperty(required = True)
    email = db.StringProperty()
    password_hash = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @classmethod
    #cls refers to the class User
    def by_id(cls, uid):
        return cls.get_by_id(uid)
    # looks up a user by name
    @classmethod
    def by_username(cls, username):
        user = cls.all().filter('username =', username).get()
        return user
    # creates the user, but does not actually store it
    @classmethod
    def register(cls, username, pw, email = None):
        pw_hash = make_pw_hash(username, pw)
        return cls(username = username,
                    password_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, username, password):
        # find user object by username
        user = cls.by_username(username)
        # if user exists and valid password
        # return user
        if user and vald_pw(username, password, user.password_hash):
            return user

#######################
####### Handler #########
#######################

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        # set cookie on Path to make sure cookies don't get set on
        # different paths
        self.response.headers.add_header(
        'Set-Cookie',
        '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    # sets the cookie to nothing
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    #called by the app engine framework
    # every request calls this function
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

##########################
####### HOME PAGE ########
##########################

class HomeHandler(Handler):
    def get(self):
        self.render("home.html")

###############################
####### MAIN BLOG PAGE ########
##############################

class MainPage(Handler):
    def render_front(self, visits):
        posts = Post.all().order('-created')
        self.render("posts.html", posts = posts, visits = visits)

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

##########################
####### NEW POST  ########
##########################

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

#################################
####### VIEW POST HANDELR #######
#################################


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

##########################
####### USER AUTH ########
##########################


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(Handler):
    def get(self):
        self.render("register.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.password_confirmation = self.request.get('password_confirmation')
        self.email = self.request.get('email')
        params = dict(username = self.username, email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username"
            have_error = True
        if not valid_password(self.password):
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email"
            have_error = True

        if have_error:
            self.render("register.html", **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError
class RegisterHandler(Signup):
    def done(self):
        user = User.by_username(self.username)
        # check to see if user is in db
        if user:
            message = 'That user aleady exists.'
            self.render('register.html', error_username = message)
        else:
            # if user dosen't exist, register user and store in db
            user = User.register(self.username, self.password, self.email)
            user.put()
            # login function sets cookie
            self.login(user)
            self.redirect('welcome')

##########################
####### Welcome  ##########
##########################
class WelcomeHandler(Handler):
    def get(self):
        # self.user is set in initialize function in Handler
        if self.user:
            self.render('welcome.html', username = self.user.username)
        else:
            self.redirect('/signup')

##########################
####### Login  ##########
##########################
class LoginHandler(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = User.login(username, password)

        if user:
            self.login(user)
            self.redirect('/welcome')
        else:
            message = 'Invaild login. Please try again.'
            self.render('login.html', error = message)

class LogoutHandler(Handler):
    def get(self):
        # calls logout method located in Handler
        self.logout()
        self.redirect('/signup')

app = webapp2.WSGIApplication([('/', HomeHandler),
                              ('/blog/?', MainPage),
                              ('/blog/newpost', NewPost),
                              (r'/blog/(\d+)', PostHandler),
                              ('/login', LoginHandler),
                              ('/signup', RegisterHandler),
                              ('/logout', LogoutHandler),
                              ('/welcome', WelcomeHandler)], debug=True)
