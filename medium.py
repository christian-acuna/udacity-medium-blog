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
from handlers.posts.edit_post import EditPostHandler
from handlers.posts.delete_post import DeletePostHandler

# handlers/sessions
from handlers.sessions.login import LoginHandler
from handlers.sessions.logout import LogoutHandler
from handlers.sessions.signup import Signup
from handlers.sessions.registration import RegisterHandler

# handlers/comments
from handlers.comments.new_comment import CommentHandler
from handlers.comments.delete_comment import DeleteCommentHandler
from handlers.comments.edit_comment import EditCommentHandler

from handlers.welcome import WelcomeHandler

app = webapp2.WSGIApplication([('/', HomeHandler),
                              ('/blog/?', MainPage),
                              ('/blog/posts/new', NewPost),
                              (r'/blog/posts/(\d+)', PostHandler),
                              (r'/blog/posts/(\d+)/edit', EditPostHandler),
                              (r'/blog/posts/(\d+)/delete', DeletePostHandler),
                               (r'/blog/posts/like', LikeHandler),
                               ('/comments', CommentHandler),
                                ('/comments/edit', EditCommentHandler),
                               ('/comments/delete', DeleteCommentHandler),
                              ('/login', LoginHandler),
                              ('/signup', RegisterHandler),
                              ('/logout', LogoutHandler),
                              ('/welcome', WelcomeHandler)], debug=True)
