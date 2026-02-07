class AccountStore:
    def __init__(self):
        self.accounts = []
    
    def load(self, path):
        pass
    
    def findAccount(self, name, accountNum):
        for account in self.accounts:
            if account.name == name and account.accountNum == str(accountNum):
                return account
        return None
