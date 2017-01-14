import json

from models.post import Post
from handlers.handler import Handler

class LikeHandler(Handler):
    """Class that is responsible for adding a like to a post"""
    def post(self):
        post_id = int(self.request.get('postID'))
        post = Post.get_by_id(post_id)
        # uid = self.user.key.id()
        #
        # if uid == post.author

        post.likes = post.likes + 1
        post.likers.append(self.user.username)

        if self.user:
            if self.user.username != post.author:
                post.put()
                self.write(json.dumps(({'likes': post.likes})))
            else:
                self.redirect("/blog")
        else:
            error = "You need to be logged in to like a post!"
            return self.render('login.html', error = error)
