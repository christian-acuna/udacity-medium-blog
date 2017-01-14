import os
import webapp2
import random
from string import letters
import re
from google.appengine.ext import db


from handlers.likes import LikeHandler
from handlers.handler import Handler
from handlers.main import MainPage
from handlers.home import HomeHandler
from handlers.new_post import NewPost
from handlers.logout import LogoutHandler
from handlers.welcome import WelcomeHandler
from handlers.post import PostHandler
from handlers.login import LoginHandler
from models.post import Post

# global render_str function that does not inherit from class Handler


#################################
####### EDIT POST HANDELR #######
#################################

class EditPostHandler(Handler):
    """Class that handles the editing of a single post"""
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if not post:
            self.error(404)
            return self.render("404.html")

        if self.user.username == post.author:
            self.render("edit_post.html", post = post, subject = post.subject, content = post.content)
        else:
            error = "You need to be logged in to edit a post!"
            return self.render('login.html', error = error)

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        subject = self.request.get('subject')
        content = self.request.get('content')

        if self.user and self.user.username == post.author:
            if subject and content:
                post.subject = subject
                post.content = content
                post.put() #store in database
                self.redirect("/blog/posts/%s" % str(post.key().id()))
            else:
                error = 'A post needs both a subject line and content'
                self.render_form(subject=subject, content=content, error=error)
        else:
            error = "You need to be logged in to edit a post!"
            return self.render('login.html', error = error)

#################################
####### EDIT POST HANDELR #######
#################################

class DeletePostHandler(Handler):
    """Class that deletes a post"""
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if self.user.username == post.author:
            post.delete()
            message = "Your post has been deleted"
            self.render("posts.html", message = message)
        else:
            error = "You need to be logged in to delete a post!"
            return self.render('login.html', error = error)


##########################
####### USER AUTH ########
##########################


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



app = webapp2.WSGIApplication([('/', HomeHandler),
                              ('/blog/?', MainPage),
                              ('/blog/posts/new', NewPost),
                              (r'/blog/posts/(\d+)', PostHandler),
                              (r'/blog/posts/(\d+)/edit', EditPostHandler),
                              (r'/blog/posts/(\d+)/delete', DeletePostHandler),
                               (r'/blog/posts/like', LikeHandler),
                              ('/login', LoginHandler),
                              ('/signup', RegisterHandler),
                              ('/logout', LogoutHandler),
                              ('/welcome', WelcomeHandler)], debug=True)
