from atm.atm import ATM

def main():
    accounts_file = "data/accounts.txt"
    input_file = "data/input.txt"
    output_file = "data/output.txt"

    atm = ATM(accounts_file, input_file, output_file)
    atm.run()
    
if __name__ == "__main__":    
    main()