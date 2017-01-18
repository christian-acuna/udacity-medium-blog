from models.user import User
from handlers.handler import Handler


class LoginHandler(Handler):

    def get(self):
        self.render("sessions/login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = User.login(username, password)

        if user:
            self.login(user)
            self.redirect('/welcome')
        else:
            message = 'Invaild login. Please try again.'
            self.render('sessions/login.html', error=message)
