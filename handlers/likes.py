"""Module for like class"""
import json

from models.post import Post
from handlers.handler import Handler

# This Handler is for likes on posts
class LikeHandler(Handler):
    """Class that is responsible for adding a like to a post"""
    def post(self):
        if self.user:
            post_id = int(self.request.get('postID'))
            post = Post.get_by_id(post_id)
            uid = self.user.key().id()
            print uid
            print post.author_id


            if uid == post.author_id:
                error = "You cannot like your own post!"
                self.write(json.dumps(({'error': error})))
            elif str(uid) in post.liked_by:
                post.likes -= 1
                post.liked_by.remove(str(uid))
                self.write(json.dumps(({'removeLikes': post.likes})))
                post.put()
            else:
                post.likes = post.likes + 1
                post.liked_by.append(str(uid))
                self.write(json.dumps(({'addLikes': post.likes})))
                post.put()
        else:
            error = 'You need to be logged in to like a post! Please <a href="/login">Log in</a>.'
            self.write(json.dumps(({'error': error})))
