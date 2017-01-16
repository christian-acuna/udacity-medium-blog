from models.post import Post
from models.user import User
from models.comment import Comment
from handlers.handler import Handler
from google.appengine.ext import db
import json

class CommentHandler(Handler):
    """Handler for creatin a new comment"""
    def post(self):
        """Only signed in users can post a comment. AJAX is used to update comments in the view"""
        if not self.user:
            self.redirect('/login')
        else:
            body = self.request.get('body')
            parent = Post.get_by_id(int(self.request.get('parent')))
            author = self.user.username
            author_id = self.user.key().id()
            if not body:
                return # return nothing
            else:
                # call class method write_entity to create comment instance
                comment = Comment.write_entity(body, author, parent, author_id)
                comment.put()
                # render HTML for response
                comment_html = self.render_comment(comment)
                self.write(json.dumps(({'comment': comment_html})))

    def render_comment(self, comment):
        """renders a comment for ajax response"""

        comment = '''
        <div  data-commentId="%s"class="comment">
            <a class="avatar">
              <img src="https://robohash.org/%s">
            </a>
            <div class="content">
              <h3 class="author">%s</h3>
              <div class="text">
                %s
              </div>
              <div class="actions">
                <a class="reply">Delete</a>
              </div>
            </div>
        </div>

        ''' % (comment.key().id(), \
               self.user.username, \
               comment.author, \
               comment.body)

        return comment
