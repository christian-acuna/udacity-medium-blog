"""Module for User class model"""
import re
import hashlib
import hmac
import random
from google.appengine.ext import db
from string import letters


class User(db.Model):
    """class for User model"""
    username = db.StringProperty(required=True)
    email = db.StringProperty()
    password_hash = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    # cls refers to the class User
    def by_id(cls, uid):
        return cls.get_by_id(uid)
    # looks up a user by name

    @classmethod
    def by_username(cls, username):
        user = cls.all().filter('username =', username).get()
        return user

    # creates the user, but does not actually store it
    @classmethod
    def register(cls, username, pw, email=None):
        pw_hash = cls.make_pw_hash(username, pw)
        return cls(username=username,
                   password_hash=pw_hash,
                   email=email)

    @classmethod
    def login(cls, username, password):
        # find user object by username
        user = cls.by_username(username)
        # if user exists and valid password
        # return user
        if user and cls.vald_pw(username, password, user.password_hash):
            return user

    # make a string of 5 letters
    @classmethod
    def make_salt(cls, length=5):
        return ''.join(random.choice(letters) for x in xrange(length))

    # makes a password hash. Takes a username and pw (with optinal param
    # for salt)
    # return salt, hashed version of (name + pw + salt)
    # store this in the database
    @classmethod
    def make_pw_hash(cls, name, pw, salt=None):
        if not salt:
            salt = cls.make_salt()
        h = hashlib.sha256(name + pw + salt).hexdigest()
        return "%s,%s" % (salt, h)

    # function to verify password
    # makes sure hash from database matches the new hash based on params
    @classmethod
    def vald_pw(cls, name, password, h):
        salt = h.split(',')[0]
        return h == cls.make_pw_hash(name, password, salt)

    @classmethod
    def valid_username(cls, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return username and USER_RE.match(username)

    @classmethod
    def valid_password(cls, password):
        PASS_RE = re.compile(r"^.{3,20}$")
        return password and PASS_RE.match(password)

    @classmethod
    def valid_email(cls, email):
        EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
        return not email or EMAIL_RE.match(email)
