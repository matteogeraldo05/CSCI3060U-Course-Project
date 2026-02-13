# In this class, 



class OutputStream:
    def __init__(self, srcPath):
        self.srcPath = srcPath

    def write(self, message):
        print(message)
    
    def writeTransactionFile(self, transactions):
        # format: CC_AAAAAAAAAAAAAAAAAAAA_NNNNN_PPPPPPPP_MM
        # _ --> is a space
        # CC --> a two-digit transaction code, 01-withdrawal, 02-transfer, 03-paybill, 
        #        04-deposit, 05-create, 06-delete, 07-disable, 08-changeplan, 00-end of session
        # NNNNN --> the bank account number
        # AAAAAAAAAAAAAAAAAAAA --> the account holder’s name
        # PPPPPPPP --> the amount of funds involved in the transaction (in CAD)
        # MM --> any additional miscellaneous information that is needed in
        #        the transaction but does not fit in any of the other fields
        
        with open(self.srcPath, 'w') as file:
            for trans in transactions:
                # Format each field according to requirements
                code = trans['code']
                name = trans['name'].ljust(20)[:20]  # alphabetic fields are left justified, filled with spaces
                account = f"{trans['account_num'].zfill(5)}" #numeric fields are right justified, filled with zeroes
                amount = f"{trans['amount']:08.2f}"  # “.00” is appended to the end of the value
                misc = trans['misc'].ljust(2)[:2]
                
                # create 40 character line
                line = f"{code} {name} {account} {amount} {misc}\n"
                file.write(line)
            
            # the sequence of transactions ends with an end of session (00) transaction code
            end_line = "00" + " " * 38 + "\n"
            file.write(end_line)