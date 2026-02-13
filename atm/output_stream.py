'''
The InputStream class manages all user input for the ATM Banking system.

This class is responsible for reading commands either from standard input
(interactive command line) or from a provided file source. It allows the
system to operate in both interactive mode and automated file-driven mode.

It maintains the current input source state, handles end-of-file transitions,
echoes file-based commands for visibility, and safely captures interruptions
to ensure controlled session termination.
'''

class OutputStream:
    def __init__(self, srcPath):
        self.srcPath = srcPath

    '''
    Writes a message to the output stream.
    In interactive mode, this simply prints the message to the console.
    '''

    def write(self, message):
        print(message)

    '''
    Writes all recorded transactions to the output file
    in the required fixed-width transaction format.

    Each transaction is formatted according to system
    specifications, including transaction code, account
    holder name, account number, amount, and miscellaneous
    information. An end-of-session transaction (00) is
    appended after all records.
    '''
    
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