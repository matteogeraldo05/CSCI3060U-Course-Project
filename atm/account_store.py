from atm.account import Account

'''
The AccountStore class is the central storage and retrieval manager 
for all Account objects within the ATM Banking system.

This class is responsible for loading account data from a formatted file,
creating Account objects, and maintaining them in memory for the duration
of the session. It provides lookup functionality to retrieve accounts 
by name, account number, or both.

It maintains the collection of active accounts and serves as the primary
access point for account queries within the system.
'''

class AccountStore:
    def __init__(self):
        self.accounts = []
    
    # load accounts from file

    '''
    Loads account records from a formatted account file.

    Reads each line from the specified file, parses the fixed-width
    account fields, creates Account objects, and stores them in memory.
    Stops loading when the END_OF_FILE marker is encountered.

    Constraints:
        - Each line must follow the fixed-width format.
        - File must contain an END_OF_FILE record.
    '''

    def load(self, path):
        with open(path, 'r') as file:
            for line in file:
                line = line.rstrip('\n')
                
                # contraint: every line is exactly 37 characters (plus newline)
                account_num = line[0:5].strip()
                name = line[6:26].strip()
                status = line[27]
                balance = float(line[29:37].strip())
                
                # constraint: file ends with a special bank account END_OF_FILE
                if name == "END_OF_FILE":
                    break
                
                #!TEMP FIX BECUASE PLAN IS NOT STORED
                plan = None

                account = Account(name,account_num, balance, status, plan)
                self.accounts.append(account)
        
    '''
    Searches for an account using both account holder name
    and account number.

    Returns the matching Account object if found. Returns None if no match is found.
    '''

    def findAccountByNameAndNumber(self, name, accountNum):
        for account in self.accounts:
            if account.name == name and account.accountNum == accountNum:
                return account
        return None
    
    '''
    Searches for an account using only the account holder name.

    Returns the matching Account object if found. Returns None if no match is found.
    '''

    def findAccountByName(self, name):
        for account in self.accounts:
            if account.name == name:
                return account
        return None

    '''
    Searches for an account using only the account number.

    Returns the matching Account object if found. Returns None if no match is found.
    '''

    def findAccountByAccountNum(self, accountNum):
        for account in self.accounts:
            if account.accountNum == accountNum:
                return account
        return None