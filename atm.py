class ATM:
    def __init__(self):
        self.balance = 0
    
    def run(self):
        while True:
            print("welcome to ATM v1.0")
            print("1. login")
            print("2. deposit")
            print("3. withdraw")
            print("4. logout")
            
            choice = input("Please select an option: ")
            
            if choice == '1':
                self.login()
            elif choice == '2':
                self.deposit()
            elif choice == '3':
                self.withdraw()
            elif choice == '4':
                self.logout()
            else:
                print("not a command, please try again")

    def login(self):
        input("Please enter your username: ")
        input("Please enter your password: ")
        print("You have logged in successfully.")

    def deposit(self):
        amount = float(input("Enter the amount to deposit: "))
        self.balance += amount
        print(f"Deposited ${amount:.2f}. Current balance: ${self.balance:.2f}")