from .session import Session
from .account_store import AccountStore
from .input_stream import InputStream
from .output_stream import OutputStream
from .record_actions import RecordActions


version = "alpha v1.4"
class ATM:
    def __init__(self, accounts_path, inputPath, outputPath):
        self.session = Session()
        self.accounts = AccountStore()
        self.inputStream = InputStream(inputPath)
        self.outputStream = OutputStream(outputPath)
        self.running = True
        self.accounts.load(accounts_path)
        self.accounts_path = accounts_path

        # log transactions to write on logout
        self.recordActions = RecordActions()

        # track session limits
        self.session_withdrawals = 0.0
        self.session_transfers = 0.0
        self.session_paybills = 0.0

    def run(self):
        self.outputStream.write(f"welcome to ATM {version}")

        while self.running:
            self.outputStream.write("\n--> login")
            self.outputStream.write("--> deposit")
            self.outputStream.write("--> withdraw")
            self.outputStream.write("--> transfer")
            self.outputStream.write("--> paybill")
            self.outputStream.write("--> create")
            self.outputStream.write("--> delete")
            self.outputStream.write("--> disable")
            self.outputStream.write("--> changeplan")
            self.outputStream.write("--> logout\n")

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
                self.paybill()
            elif cli_choice == "create":
                self.create()
            elif cli_choice == "delete":
                self.delete()
            elif cli_choice == "disable":
                self.disable()
            elif cli_choice == "changeplan":
                self.changeplan()
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
            if not self.accounts.findAccountByName(account_name):
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
        self.outputStream.writeTransactionFile(self.recordActions.get_transactions())

        # clear session data
        self.session.loggedIn = False
        self.session.isAdmin = False
        self.session.accountHolderName = None
        self.recordActions.clear_transactions()

        # reset session limits
        self.session_withdrawals = 0.0
        self.session_transfers = 0.0
        self.session_paybills = 0.0
        
        self.outputStream.write("logged out successfully")
        self.outputStream.write(f"thank you for using ATM {version}!")
        self.running = False

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

        # check if account disabled
        if account.status == "D":
            self.outputStream.write(f"error: Account {account_num} is disabled")
            return
        
        # then should ask for the amount to deposit
        self.outputStream.write("enter deposit amount:")
        amount = float(self.inputStream.readNextLine())
        
        # check number is positive
        if amount <= 0:
            self.outputStream.write("error: amount must be positive")
            return
        
        # consrtaint: Deposited funds should not be available for use in this session
        self.outputStream.write(f"deposited ${amount:.2f} to account {account_num}. funds will be available after logout")
        
        # should save this information for the bank account transaction file
        self.recordActions.record_transaction("04", account_name, account_num, amount, "")

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

        # check if account disabled
        if account.status == "D":
            self.outputStream.write(f"error: Account {account_num} is disabled")
            return
        
        # then should ask for the amount to withdraw
        self.outputStream.write("enter withdraw amount:")
        amount = float(self.inputStream.readNextLine())
        
        # check number is positive
        if amount <= 0:
            self.outputStream.write("error: amount must be positive")
            return

        # consrtaint: Maximum amount that can be withdrawn in current session is $500.00 in standard mode
        if not self.session.isAdmin:
            if self.session_withdrawals + amount > 500.00:
                self.outputStream.write(f"withdrawal exceeds session limit. remaining: ${500.00 - self.session_withdrawals:.2f}")
                return
        
        # constraint: Account balance must be at least $0.00 after withdrawal
        if account.balance < amount:
            self.outputStream.write("insufficient funds for withdrawal")
            return
        
        # withdraw funds from account balance
        account.balance -= amount

        # add to session withdrawls count
        if not self.session.isAdmin:
            self.session_withdrawals += amount

        self.outputStream.write(f"withdrew ${amount:.2f} from account {account_num}. funds will be available after logout")
        
        # should save this information for the bank account transaction file
        self.recordActions.record_transaction("01", account_name, account_num, amount, "")

    def transfer(self):
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
        if not self.session.isAdmin:
            if self.session_transfers + transfer_amount > 1000.00:
                self.outputStream.write(f"transfer exceeds session limit. remaining: ${1000.00 - self.session_transfers:.2f}")
                return

        # find sender account
        accountSender = self.accounts.findAccountByNameAndNumber(account_name, account_sender_num)
        if not accountSender:
            self.outputStream.write(f"sender account not found for '{account_name}' with account number '{account_sender_num}'")
            return
        
        # check if sender account is disabled
        if accountSender.status == 'D':
            self.outputStream.write(f"Error: Sender account {account_sender_num} is disabled.")
            return
        
        # find receiver account
        accountReceiver = self.accounts.findAccountByAccountNum(account_reciever_num)
        if not accountReceiver:
            self.outputStream.write(f"receiver account {account_reciever_num} not found")
            return
        
        # check if receiver account is disabled
        if accountReceiver.status == 'D':
            self.outputStream.write(f"Error: Receiver account {account_reciever_num} is disabled.")
            return

        # constraint: Sender balance must be at least $0.00 after withdrawal
        if accountSender.balance < transfer_amount:
            self.outputStream.write("Sender has insufficient funds for transfer")
            return

        # constraint: Reciever balance must be at least $0.00 after withdrawal
        if accountReceiver.balance + transfer_amount < 0:
            self.outputStream.write("Reciever has insufficient funds for transfer")
            return

        accountSender.balance = accountSender.balance - transfer_amount
        accountReceiver.balance = accountReceiver.balance + transfer_amount

        # add to session transfers count
        if not self.session.isAdmin:
            self.session_transfers += transfer_amount

        # Record Transfer
        self.recordActions.record_transfer(code="02", account_num_sender=account_sender_num, 
                             account_num_reciever=account_reciever_num, amount=transfer_amount, misc=None, name=account_name)

        self.outputStream.write("Transaction Completed")
        return

    def paybill(self):
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

        # check if account disabled
        if account.status == 'D':
            self.outputStream.write(f"Error: Account {account_num} is disabled.")
            return
        
        # should ask for the company to whom the bill is being paid
        self.outputStream.write("Enter company (EC/CQ/FI):")
        company_code = self.inputStream.readNextLine().strip().upper()

        # constraint: The company to whom the bill is being paid must be “The Bright Light Electric Company (EC)”, “Credit Card Company Q (CQ)” or “Fast Internet, Inc. (FI)”
        valid_companies = {
            "EC": "The Bright Light Electric Company",
            "CQ": "Credit Card Company Q",
            "FI": "Fast Internet, Inc."
        }

        if company_code not in valid_companies:
            self.outputStream.write("error: Invalid company. must be EC, CQ, or FI")
            return
        
        # should ask for the amount to pay
        self.outputStream.write("enter bill amount:")
        amount = float(self.inputStream.readNextLine().strip())

        # check that number is positive
        if amount <= 0:
            self.outputStream.write("Error: Amount must be positive.")
            return
        
        # constraint: maximum amount that can be paid to a bill holder in current session is $2000.00 in standard mode
        if not self.session.isAdmin:
            if self.session_paybills + amount > 2000.00:
                self.outputStream.write(f"bill payment exceeds session limit. remaining: ${2000.00 - self.session_paybills:.2f}")
                return
            
        # constraint: account balance must be at least $0.00 after bill is paid
        if account.balance < amount:
            self.outputStream.write("error: Insufficient funds")
            return
        
        # withdraw funds from account balance to pay bill
        account.balance -= amount

        # add to session bill payments count
        if not self.session.isAdmin:
            self.session_paybills += amount

        self.outputStream.write(f"withdrew ${amount:.2f} from account {account_num} to pay bill")
        
        # should save this information for the bank account transaction file
        self.recordActions.record_transaction("03", account_name, account_num, amount, company_code)
        
    def create(self):
        # constraint: privileged transaction - only accepted when logged in admin mode
        if not self.session.loggedIn:
            self.outputStream.write("not logged in. please login first")
            return
        
        if not self.session.isAdmin:
            self.outputStream.write("Error: Admin privileges required")
            return 

        # should read the last account number from the accounts file
        with open(self.accounts_path, "r") as file:
            lines = file.readlines()
    
        # constraint: bank account numbers must be unique in the Bank System
        # increment the last account number to create a new unique account number
        final_acc = lines[-1][0:5].strip("0")
        acc_num = int(final_acc) + 1
        acc_num = f"{acc_num:05d}"

        # should set the account status to active (A)
        acc_status = "A"

        # should ask for the name of the account holder (as a text line)
        self.outputStream.write("Input New Account Name (max 20 characters):")
        acc_name = self.inputStream.readNextLine().strip()

        # constraint: new account holder name is limited to at most 20 characters
        if len(acc_name) > 20:
            self.outputStream.write("Error: Name larger than 20 characters")
            return
        
        # format the account holder name to fixed width
        acc_name = f"{acc_name:<20}"[:19]

        # should ask for the initial balance of the account
        self.outputStream.write("Initial Balance (max $99999.99):")
        acc_balance = float(self.inputStream.readNextLine())
        
        # constraint: account balance can be at most $99999.99
        if acc_balance < 0 or acc_balance > 99999.99:
            self.outputStream.write("Error: Balance number out of range ($0 - $99999.99)")
            return
        
        # format the balance to fixed width currency field
        acc_balance_str = f"{acc_balance:08.2f}"

        # write the new account to the file
        with open(self.accounts_path, "a") as file:
            full_acc = f"{acc_num} {acc_name} {acc_status} {acc_balance_str}\n"
            file.write(full_acc)
       
        # record create account to transaction file
        self.recordActions.record_transaction("05", acc_name.strip(), acc_num, acc_balance, "")

        self.outputStream.write(f"Account created: {acc_num} for {acc_name.strip()} with balance ${acc_balance:.2f}")
        self.outputStream.write("Note: This account will not be available for transactions until next session")

    def delete(self):
        # constraint: privileged transaction - only accepted when logged in admin mode
        if not self.session.loggedIn:
            self.outputStream.write("not logged in. please login first")
            return
        
        if not self.session.isAdmin:
            self.outputStream.write("Error: Admin privileges required")
            return
        
        # ask for the bank account holder's name (as a text line)
        self.outputStream.write("Enter account holder name:")
        account_name = self.inputStream.readNextLine().strip()
        
        # constraint: name limited to 20 characters
        if len(account_name) > 20:
            self.outputStream.write("Error: Name too long (max 20 characters)")
            return
        
        # format name to fixed width 20 characters for file comparison
        account_name_formatted = f"{account_name:<20}"[:20]

        # ask for the account number (as a text line)
        self.outputStream.write("Enter account number:")
        account_num = self.inputStream.readNextLine().strip()
        
        # constraint: account number must be 5 digits
        if len(account_num) != 5 or not account_num.isdigit():
            self.outputStream.write("Error: Invalid account number format (must be 5 digits)")
            return
        
        # read all existing accounts from the file
        with open(self.accounts_path, "r") as file:
            lines = file.readlines()
        
        # filter the account to be deleted
        found = False
        new_lines = []
        for line in lines:
            # extract account number and account holder name from line
            line_acc_num = line[0:5]
            line_name = line[6:26]
            # if line matches the account to delete, skip it
            if line_acc_num == account_num and line_name.lower() == account_name_formatted.lower():
                found = True
                continue
            # otherwise, keep the line
            new_lines.append(line.rstrip("\n"))

        # if the account was not found, output error and return
        if not found:
            self.outputStream.write(f"No account found for {account_name} with account number {account_num}")
            return 

        # write the remaining accounts back to the file, effectively deleting the chosen account
        try:
            with open(self.accounts_path, "w") as file:
                for line in new_lines:
                    file.write(line + "\n")
        except Exception as e:
            self.outputStream.write(f"Error writing accounts file: {e}")
            return

        # record transaction for account deletion
        self.recordActions.record_transaction("06", account_name, account_num, 0.0, "")

        self.outputStream.write(f"Account {account_num} for {account_name} has been deleted.")

    def disable(self):
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
        self.recordActions.record_transaction("07", account_name, account_num, 0.0, "")
    
        self.outputStream.write(f"account {account_num} for {account_name} has been disabled") 
                
    def changeplan(self):
        if not self.session.loggedIn:
            self.outputStream.write("not logged in. please login first")
            return
        
        # constraint: privileged transaction - only accepted when logged in admin mode
        if not self.session.isAdmin:
            self.outputStream.write("Error: This is a privileged transaction. Admin access required.")
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
        
        # should set the bank account payment plan from student (SP) to non-student (NP)
        if account.plan == "SP":
            account.plan = "NP"
            self.outputStream.write(f"account plan changed from Student to Non-Student for account {account_num}")
        elif account.plan == "NP":
            account.plan = "SP"
            self.outputStream.write(f"account plan changed from Non-Student to Student for account {account_num}")
        else:
            self.outputStream.write(f"account {account_num} has an invalid plan")
            return

        # should save this information for the bank account transaction file

        self.recordActions.record_transaction("08", account_name, account_num, 0.0, "")