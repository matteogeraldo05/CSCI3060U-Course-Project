from atm.atm import ATM
'''
Main class used to run the program

This class holds specifies where the data is stored.
It then initiates an ATM which loads the data from the text base.

The ATM is then run which then acts as a front end for the banking system.
'''
def main():
    accounts_file = "data/accounts.txt"
    input_file = "data/input.txt"
    output_file = "data/output.txt"

    atm = ATM(accounts_file, input_file, output_file)
    atm.run()
    
if __name__ == "__main__":    
    main()