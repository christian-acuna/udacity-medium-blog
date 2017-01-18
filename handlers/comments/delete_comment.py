from models.post import Post
from models.user import User
from models.comment import Comment
from handlers.handler import Handler
from google.appengine.ext import db
import json


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
