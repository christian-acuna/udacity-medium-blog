from models.user import User
from handlers.handler import Handler
from google.appengine.ext import db


class Signup(Handler):

    def get(self):
        self.render("sessions/register.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.password_confirmation = self.request.get('password_confirmation')
        self.email = self.request.get('email')
        params = dict(username=self.username, email=self.email)

        if not User.valid_username(self.username):
            params['error_username'] = "That's not a valid username"
            have_error = True

        if not User.valid_password(self.password):
            params['error_password_valid'] = "Password is not valid"
            have_error = True
        elif self.password != self.password_confirmation:
            params['error_pw_match'] = "Passwords do not match"
            have_error = True

        if not User.valid_email(self.email):
            params['error_email'] = "That's not a valid email"
            have_error = True

        if User.by_username(self.username):
            params['error_user_exits'] = 'That user aleady exists.'
            have_error = True

        if have_error:
            print params
            params['error'] = True
            self.render("sessions/register.html", **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError
