from handlers.handler import Handler

class HomeHandler(Handler):
    """Class that renders the root home page"""
    def get(self):
        self.render("home.html")
