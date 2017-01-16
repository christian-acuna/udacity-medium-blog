from handlers.sessions.signup import Signup
from models.user import User

class RegisterHandler(Signup):
    def done(self):
        # check to see if user is in db
        # if user dosen't exist, register user and store in db
        user = User.register(self.username, self.password, self.email)
        user.put()
        # login function sets cookie
        self.login(user)
        self.redirect('welcome')
