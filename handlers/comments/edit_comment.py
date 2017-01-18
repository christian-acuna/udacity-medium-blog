from models.post import Post
from models.user import User
from models.comment import Comment
from handlers.handler import Handler
from google.appengine.ext import db
import json

class EditCommentHandler(Handler):
    """Class that edits a comment via AJAX"""
    def post(self):
        if not self.user:
            self.redirect('/login')
        else:
            comment_id = self.request.get('commentId')
            post_id = self.request.get('postId')
            comment_text = self.request.get('commentText')
            parent_key = Post.get_by_id(int(post_id))
            comment = Comment.get_by_id(int(comment_id), parent_key)

            if comment and self.user and self.user.key().id() == comment.author_id:
                comment.body = comment_text
                comment.put()

                self.write(json.dumps(({'comment': comment.key().id()})))
            else:
                error = "There was an editing the comment."
                self.write(json.dumps(({'error': error})))
