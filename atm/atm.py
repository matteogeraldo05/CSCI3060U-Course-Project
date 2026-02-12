from .session import Session
from .account_store import AccountStore
from .input_stream import InputStream
from .output_stream import OutputStream

version = "alpha v1.2"
class ATM:
    def __init__(self, accounts_path, inputPath, outputPath):
        self.session = Session()
        self.accounts = AccountStore()
        self.inputStream = InputStream(inputPath)
        self.outputStream = OutputStream(outputPath)
        self.running = True
        self.accounts.load(accounts_path)

        # log transactions to write on logout
        self.transactions = []
        self.transfers = []
    
    def run(self):
        self.outputStream.write(f"welcome to ATM {version}")

        while self.running:
            self.outputStream.write("\n1. login")
            self.outputStream.write("2. deposit")
            self.outputStream.write("3. withdraw")
            self.outputStream.write("4. transfer")
            self.outputStream.write("5. pay bill")
            self.outputStream.write("6. create account")
            self.outputStream.write("7. disable account")
            self.outputStream.write("8. change plan")
            self.outputStream.write("9. logout")
            self.outputStream.write("10. exit\n")

            cli_choice = self.inputStream.readNextLine().strip().lower()
            
            if cli_choice == "login":
                self.login()
            elif cli_choice == "logout":
                self.logout()
            elif cli_choice == "withdraw":
                self.withdraw()
            elif cli_choice == "deposit":
                self.deposit()
            elif cli_choice == "transfer":
                self.transfer()
            elif cli_choice == "paybill":
                self.pay_bill()
            elif cli_choice == "create account":
                self.create_account()
            elif cli_choice == "disable account":
                self.disable_account()
            elif cli_choice == "change plan":
                self.change_plan()
            elif cli_choice == "exit":
                self.exit()
            else:
                self.outputStream.write("not an option, try again")

    def login(self):    
        # constraint: no subsequent login should be accepted after a login, until after a logout
        if self.session.loggedIn:
            self.outputStream.write("already logged in. please logout first")
            return
        
        self.outputStream.write("Enter session type 'standard' or 'admin':")
        session_type = self.inputStream.readNextLine().strip().lower()
        
        if session_type == "admin":
            self.session.loggedIn = True
            self.session.isAdmin = True
            self.outputStream.write("logged in as admin")
            
        elif session_type == "standard":
            self.outputStream.write("enter account holder name:")
            account_name = self.inputStream.readNextLine().strip()
                        
            # check if account holder exists
            if not self.accounts.findAccountByNameAndNumber(account_name, None):
                self.outputStream.write(f"no account found for '{account_name}'")
                return
            
            self.session.loggedIn = True
            self.session.isAdmin = False
            self.session.accountHolderName = account_name
            self.outputStream.write(f"Logged in as {account_name}")
            
        else:
            self.outputStream.write("not an option, try 'standard' or 'admin'")
            return

    def logout(self):    
        # constraint: should only be accepted when logged in
        if not self.session.loggedIn:
            self.outputStream.write("not logged in. please login first")
            return
        
        # should write out the bank account transaction file 
        self.outputStream.writeTransactionFile(self.transactions)

        # clear session data
        self.session.loggedIn = False
        self.session.isAdmin = False
        self.session.accountHolderName = None
        self.transactions = []
        self.outputStream.write("logged out successfully")

    def deposit(self):
        # constraint: bank account must be a valid account for the account holder currently logged in.
        if not self.session.loggedIn:
            self.outputStream.write("not logged in. please login first")
            return

        # should ask for the account holder’s name (if logged in as admin)
        if self.session.isAdmin:
            self.outputStream.write("enter account holder name:")
            account_name = self.inputStream.readNextLine().strip()
        else:
            account_name = self.session.accountHolderName

        # should ask for the account number (as a text line)
        self.outputStream.write("enter account number:")
        account_num = self.inputStream.readNextLine().strip()

        # find account
        account = self.accounts.findAccountByNameAndNumber(account_name, account_num)
        if not account:
            self.outputStream.write(f"no account found for '{account_name}' with account number '{account_num}'")
            return

        # then should ask for the amount to deposit
        self.outputStream.write("enter deposit amount:")
        amount = float(self.inputStream.readNextLine())
        
        # consrtaint: Deposited funds should not be available for use in this session
        self.outputStream.write(f"deposited ${amount:.2f} to account {account_num}. funds will be available after logout")
        
        # should save this information for the bank account transaction file
        self.record_transaction("04", account_name, account_num, amount, "")

    def withdraw(self):
        # constraint: bank account must be a valid account for the account holder currently logged in.
        if not self.session.loggedIn:
            self.outputStream.write("not logged in. please login first")
            return

        # should ask for the account holder’s name (if logged in as admin)
        if self.session.isAdmin:
            self.outputStream.write("enter account holder name:")
            account_name = self.inputStream.readNextLine().strip()
        else:
            account_name = self.session.accountHolderName

        # should ask for the account number (as a text line)
        self.outputStream.write("enter account number:")
        account_num = self.inputStream.readNextLine().strip()

        # find account
        account = self.accounts.findAccountByNameAndNumber(account_name, account_num)
        if not account:
            self.outputStream.write(f"no account found for '{account_name}' with account number '{account_num}'")
            return

        # then should ask for the amount to withdraw
        self.outputStream.write("enter withdraw amount:")
        amount = float(self.inputStream.readNextLine())
        
        # consrtaint: Maximum amount that can be withdrawn in current session is $500.00 in standard mode
        if not self.session.isAdmin and amount > 500:
            self.outputStream.write("withdrawal amount exceeds $500.00 limit for standard mode")
            return
        
        # constraint: Account balance must be at least $0.00 after withdrawal
        if account.balance < amount:
            self.outputStream.write("insufficient funds for withdrawal")
            return
        
        # withdraw funds from account balance
        account.balance -= amount
        self.outputStream.write(f"withdrew ${amount:.2f} from account {account_num}. funds will be available after logout")
        
        # should save this information for the bank account transaction file
        self.record_transaction("01", account_name, account_num, amount, "")

    def transfer(self):
        # self.outputStream.write("placeholder for transfer...")

        # constraint: bank account must be a valid account for the account holder currently logged in.
        if not self.session.loggedIn:
            self.outputStream.write("not logged in. please login first")
            return

        # should ask for the account holder’s name (if logged in as admin)
        if self.session.isAdmin:
            self.outputStream.write("enter account holder name:")
            account_name = self.inputStream.readNextLine().strip()
        else:
            account_name = self.session.accountHolderName


        
        # get the account number of the money sender
        self.outputStream.write("enter account number to transfer money from")
        account_sender_num = self.inputStream.readNextLine().strip()

        # get the account number of the money reciever
        self.outputStream.write("enter account number to transfer money to")
        account_reciever_num = self.inputStream.readNextLine().strip()

        # get the amount that will be transferred 
        self.outputStream.write("enter transfer amount:")
        transfer_amount = float(self.inputStream.readNextLine())

        # constraint : can't transfer 0 or less dollars
        if transfer_amount <= 0:
            self.outputStream.write("can't transfer 0 or less dollars")
            return

        # constraint : standard accounts can't transfer more than 1000 dollars
        if (not self.session.isAdmin) and (transfer_amount > 1000):
            self.outputStream.write("can't withdraw more than 1000 in standard mode")
            return

        accountSender = self.accounts.findAccount(account_sender_num)
        accountReciever = self.accounts.findAccount(account_reciever_num)

        # constraint: Sender balance must be at least $0.00 after withdrawal
        if accountSender.balance < transfer_amount:
            self.outputStream.write("Sender has insufficient funds for withdrawal")
            return

        # constraint: Reciever balance must be at least $0.00 after withdrawal
        if accountReciever.balance < transfer_amount:
            self.outputStream.write("Sender has insufficient funds for withdrawal")
            return

        accountSender.balance = accountSender.balance - transfer_amount
        accountReciever.balance = accountSender.balance + transfer_amount 

        # Record Transfer
        self.record_transfer(self, code="4", account_num_sender=account_sender_num, 
                             account_num_reciever=account_reciever_num, amount=transfer_amount, name=account_name)

        self.outputStream.write("Transaction Completed")
        return


    def pay_bill(self):
        self.outputStream.write("enter bill amount:")
        amount = float(self.inputStream.readNextLine())
        if amount > self.balance:
            self.outputStream.write("insufficient funds")
        else:
            self.balance -= amount
            self.outputStream.write(f"paid bill of ${amount:.2f}")
            self.display_current_balance()

    def create_account(self):
        self.outputStream.write("placeholder for creating a new account...")

    def disable_account(self):
        # constraint: privileged transaction - only accepted when logged in admin mode
        if not self.session.loggedIn:
            self.outputStream.write("not logged in. please login first")
            return
        
        if not self.session.isAdmin:
            self.outputStream.write("not an admin. access denied")
            return
        
        # should ask for the bank account holder’s name (as a text line)
        self.outputStream.write("enter account holder name:")
        account_name = self.inputStream.readNextLine().strip()
        
        # should ask for the account number (as a text line)
        # constraint: account number must be the number of the account holder specified
        self.outputStream.write("enter account number:")
        account_num = self.inputStream.readNextLine().strip()

        # constraint: account holder’s name must be the name of an existing account holder
        account = self.accounts.findAccountByNameAndNumber(account_name, account_num)
        if not account:
            self.outputStream.write(f"no account found for '{account_name}' with account number '{account_num}'")
            return

        # should change the bank account from active (A) to disabled (D)
        account.status = "D"

        # should save this information for the bank account transaction file
        self._record_transaction("07", account_name, account_num, 0.0, "")
    
        self.outputStream.write(f"Account {account_num} for {account_name} has been disabled.") 
                
    def change_plan(self):
        self.outputStream.write("placeholder for changing plan...")

    def exit(self):
        if self.session.loggedIn:
            self.outputStream.write("please logout before exiting")
            return
        
        self.outputStream.write(f"thank you for using ATM {version}!")
        self.running = False
    
    def record_transaction(self, code, name, account_num, amount, misc):
        transaction = {
            'code': code,
            'name': name,
            'account_num': account_num,
            'amount': amount,
            'misc': misc
        }
        self.transactions.append(transaction)

    def record_transfer(self, code,  account_num_sender, account_num_reciever, amount, misc,name="Standard_Account"):
        transaction = {
            'code': code,
            'name': name,
            'account_num_sender': account_num_sender,
            'account_num_reciever' : account_num_reciever,
            'amount': amount,
            'misc': misc
        }
        self.transactions.append(transaction)
    def display_current_balance(self):
        self.outputStream.write(f"current balance: ${self.balance:.2f}")