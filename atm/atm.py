from .session import Session
from .account_store import AccountStore
from .input_stream import InputStream
from .output_stream import OutputStream

class ATM:
    def __init__(self, accounts_path, inputPath, outputPath):
        self.session = Session()
        self.accounts = AccountStore()
        self.inputStream = InputStream(inputPath)
        self.outputStream = OutputStream(outputPath)
        self.running = True
        self.accounts.load(accounts_path)
        #TEMPORARY
        self.balance = 0.0
    
    def run(self):
        self.outputStream.write("welcome to ATM v1.0")

        while self.running:
            self.outputStream.write("\n1. login")
            self.outputStream.write("2. deposit")
            self.outputStream.write("3. withdraw")
            self.outputStream.write("4. transfer")
            self.outputStream.write("5. pay bill")
            self.outputStream.write("6. create new account")
            self.outputStream.write("7. delete account")
            self.outputStream.write("8. change plan")
            self.outputStream.write("9. logout")

            choice = self.inputStream.readNextLine()
            
            if choice == "1":
                self.login()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.transfer()
            elif choice == "5":
                self.pay_bill()
            elif choice == "6":
                self.create_account()
            elif choice == "7":
                self.delete_account()
            elif choice == "8":
                self.change_plan()
            elif choice == "9":
                self.logout()
            else:
                self.outputStream.write("not an option, try again")

    def display_current_balance(self):
        self.outputStream.write(f"current balance: ${self.balance:.2f}")

    def login(self):
        self.outputStream.write("enter username:")
        username = self.inputStream.readNextLine()
        self.outputStream.write("enter password:")
        password = self.inputStream.readNextLine()
        self.outputStream.write("you have logged in successfully.")

    def deposit(self):
        self.outputStream.write("enter deposit amount:")
        amount = float(self.inputStream.readNextLine())
        self.balance += amount
        self.outputStream.write(f"deposited ${amount:.2f}")
        self.display_current_balance()

    def withdraw(self):
        self.outputStream.write("enter withdrawal amount:")
        amount = float(self.inputStream.readNextLine())
        if amount > self.balance:
            self.outputStream.write("insufficient funds.")
        else:
            self.balance -= amount
            self.outputStream.write(f"withdrew ${amount:.2f}")
            self.display_current_balance()

    def transfer(self):
        self.outputStream.write("enter transfer amount:")
        amount = float(self.inputStream.readNextLine())
        if amount > self.balance:
            self.outputStream.write("insufficient funds")
        else:
            self.balance -= amount
            self.outputStream.write(f"transferred ${amount:.2f}")
            self.display_current_balance()

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

    def delete_account(self):
        self.outputStream.write("placeholder for deleting account...")
                
    def change_plan(self):
        self.outputStream.write("placeholder for changing plan...")

    def logout(self):
        self.outputStream.write("you have logged out successfully")
        self.running = False