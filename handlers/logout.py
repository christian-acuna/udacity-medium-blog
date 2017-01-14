from handlers.handler import Handler

class LogoutHandler(Handler):
    def get(self):
        # calls logout method located in Handler
        self.logout()
        self.redirect('/signup')
