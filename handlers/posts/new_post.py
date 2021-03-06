from models.post import Post
from handlers.handler import Handler


class NewPost(Handler):
    """Class that is responsible for showing a new post form and
    creating a new post in  the database"""

    def render_form(self, subject="", content="", error=""):
        if self.user:
            self.render("posts/new_post.html", subject=subject,
                        content=content, error=error)
        else:
            error = "Only logged in users can write a post. Please log in."
            self.render("sessions/login.html", error=error)

    def get(self):
        self.render_form()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        # check to see if user is logged in for POST request
        if self.user:
            author = self.user.username
            author_id = self.user.key().id()
            likes = 0

            if subject and content:
                post = Post(subject=subject, content=content, author=author,
                            likes=likes, author_id=author_id)
                post.put()  # store in database
                id = post.key().id()
                self.redirect("/blog/posts/%s" % str(id))
            else:
                error = 'A post needs both a subject line and content'
                self.render_form(subject=subject, content=content, error=error)
        else:
            error = "Only logged in users can create a new post. Please log in."
            self.render("sessions/login.html", error=error)
