import os
import webapp2

import re
import json
from google.appengine.ext import db

# handlers
from handlers.handler import Handler
from handlers.main import MainPage
from handlers.home import HomeHandler
from handlers.likes import LikeHandler

# handlers/posts
from handlers.posts.new_post import NewPost
from handlers.posts.post import PostHandler

# handlers/sessions
from handlers.sessions.login import LoginHandler
from handlers.sessions.logout import LogoutHandler

# handlers/comments
from handlers.comments.new_comment import CommentHandler

from handlers.welcome import WelcomeHandler

# models
from models.post import Post
from models.user import User
from models.comment import Comment




class DeleteCommentHandler(Handler):
    """Class that deletes a comment via AJAX"""
    def post(self):
        if not self.user:
            self.redirect('/login')
        else:
            comment_id = self.request.get('commentId')
            post_id = self.request.get('postId')
            parent_key = Post.get_by_id(int(post_id))
            comment = Comment.get_by_id(int(comment_id), parent_key)
            print comment

            if self.user and self.user.key().id() == comment.author_id:
                self.write(json.dumps(({'comment': comment.key().id()})))
                comment.delete()
            else:
                error = "There was an error deleting the comment."
                self.write(json.dumps(({'error': error})))

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

        if self.user.key().id() == post.author_id:
            self.render("posts/edit_post.html", post = post, subject = post.subject, content = post.content)
        elif self.user:
            message = "You can only edit your own posts."
            posts = Post.all().order('-created')
            self.render('posts/posts.html', posts=posts, message = message )
        else:
            error = "You need to be logged in to edit a post!"
            return self.render('sessions/login.html', error = error)

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        subject = self.request.get('subject')
        content = self.request.get('content')

        if self.user and self.user.key().id() == post.author_id:
            if subject and content:
                post.subject = subject
                post.content = content
                post.put() #store in database
                self.redirect("/blog/posts/%s" % str(post.key().id()))
            else:
                error = 'A post needs both a subject line and content'
                self.render_form(subject=subject, content=content, error=error)
        elif self.user:
            message = "You can only edit your own posts."
            posts = Post.all().order('-created')
            self.render('posts/posts.html', posts=posts, message = message )
        else:
            error = "You need to be logged in to edit a post!"
            return self.render('sessions/login.html', error = error)

#################################
####### EDIT POST HANDELR #######
#################################

class DeletePostHandler(Handler):
    """Class that deletes a post"""
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if self.user and self.user.key().id() == post.author_id:
            post.delete()
            self.redirect('/welcome?msg=1')
        elif self.user:
            self.redirect('/blog?error=1')
        else:
            error = "You need to be logged in to delete a post!"
            return self.render('sessions/login.html', error = error)


##########################
####### USER AUTH ########
##########################


class Signup(Handler):
    def get(self):
        self.render("sessions/register.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.password_confirmation = self.request.get('password_confirmation')
        self.email = self.request.get('email')
        params = dict(username = self.username, email = self.email)

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

class RegisterHandler(Signup):
    def done(self):
        # check to see if user is in db
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
                               ('/comments', CommentHandler),
                               ('/comments/delete', DeleteCommentHandler),
                              ('/login', LoginHandler),
                              ('/signup', RegisterHandler),
                              ('/logout', LogoutHandler),
                              ('/welcome', WelcomeHandler)], debug=True)
