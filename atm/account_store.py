from atm.account import Account

class AccountStore:
    def __init__(self):
        self.accounts = []
    
    # load accounts from file
    def load(self, path):
        with open(path, 'r') as file:
            for line in file:
                line = line.rstrip('\n')
                
                # contraint: every line is exactly 37 characters (plus newline)
                account_num = int(line[0:5].strip())
                name = line[6:26].strip()
                status = line[27]
                balance = float(line[29:37].strip())
                
                # constraint: file ends with a special bank account END_OF_FILE
                if name == "END_OF_FILE":
                    break
                
                account = Account(name,account_num, balance, status)
                self.accounts.append(account)
        
    # Find account given name and accountNum
    def findAccountByNameAndNumber(self, name, accountNum):
        for account in self.accounts:
            if account.name == name and account.accountNum == accountNum:
                return account
        return None
    
    # Find account only given name
    def findAccountByName(self, name):
        for account in self.accounts:
            if account.name == name:
                return account
        return None

    # Find account only given account num
    def findAccountByAccountNum(self, accountNum):
        for account in self.accounts:
            if account.accountNum == accountNum:
                return account
        return None


    def generateNewAccount(self):
        # format: NNNNN_AAAAAAAAAAAAAAAAAAAA_S_PPPPPPPP
        # _ --> is a space
        # NNNNN --> the bank account number
        # AAAAAAAAAAAAAAAAAAAA --> the account holder’s name
        # S --> the bank account status – active (A) or disabled (D)
        # PPPPPPPP --> the current balance of the account (in Canadian dollars)
        pass