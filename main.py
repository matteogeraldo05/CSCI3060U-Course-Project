from atm.atm import ATM
'''
Main class used to run the program

This class holds specifies where the data is stored.
It then initiates an ATM which loads the data from the text base.
The ATM interface has several options. 

- User Authentications
    - Asks for a Login, assures it exists in the database

- Handles Transactions
    - Deposit
    - Withdraw
    - Transfer
    - Pay Bill

- Administrative Operations
    - Create : creates a new account for the banking system
    - Delete : Remove accounts
    - Disable : Deactivate an account
    - Change Plan : Toggle between Student and non-student account 

The ATM is then run which then acts as a front end for the banking system.

HOW TO USE:
    The ATM will prompt the user for information (ex account name or money amount)
    The user then types the requires information and the ATM will verify if the operation can be conducted

LOGOUT:
    When logged out, the ATM refreshed and updates transaction logs.
'''
def main():
    accounts_file = "data/accounts.txt"
    output_file = "data/output.txt"

    atm = ATM(accounts_file, output_file)
    atm.run()
    
if __name__ == "__main__":    
    main()