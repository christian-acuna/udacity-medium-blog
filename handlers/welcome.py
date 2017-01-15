from handlers.handler import Handler

class WelcomeHandler(Handler):
    def get(self):
        # self.user is set in initialize function in Handler
        if self.user:
            self.render('welcome.html', username = self.user.username)
        else:
            self.redirect('/signup')
