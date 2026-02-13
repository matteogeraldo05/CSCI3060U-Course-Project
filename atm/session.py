'''
Object to specify session details. Loaded when the ATM class is loaded

Specifies the following

- If the session is in a logged in state
- If the logged in state has admin control

'''
class Session:
    def __init__(self):
        self.loggedIn = False
        self.isAdmin = False
