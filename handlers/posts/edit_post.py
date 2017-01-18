from models.post import Post
from handlers.handler import Handler
from google.appengine.ext import db


class EditPostHandler(Handler):
    """Class that handles the editing of a single post"""

    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if not post:
            return self.redirect('/blog?error=2')

        if self.user.key().id() == post.author_id:
            self.render("posts/edit_post.html", post=post,
                        subject=post.subject, content=post.content)
        elif self.user:
            message = "You can only edit your own posts."
            posts = Post.all().order('-created')
            self.render('posts/posts.html', posts=posts, message=message)
        else:
            error = "You need to be logged in to edit a post!"
            return self.render('sessions/login.html', error=error)

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        subject = self.request.get('subject')
        content = self.request.get('content')

        if self.user and self.user.key().id() == post.author_id:
            if subject and content:
                post.subject = subject
                post.content = content
                post.put()  # store in database
                self.redirect("/blog/posts/%s" % str(post.key().id()))
            else:
                error = 'A post needs both a subject line and content'
                self.render_form(subject=subject, content=content, error=error)
        elif self.user:
            message = "You can only edit your own posts."
            posts = Post.all().order('-created')
            self.render('posts/posts.html', posts=posts, message=message)
        else:
            error = "You need to be logged in to edit a post!"
            return self.render('sessions/login.html', error=error)
