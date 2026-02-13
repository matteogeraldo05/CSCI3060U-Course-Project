'''
The RecordActions class is responsible for tracking all transactional
activity during an ATM session.

This class records deposits, withdrawals, transfers, and other account-related
operations in a structured format. Each action is stored in memory until
the user logs out, at which point the collected records can be written to
an output file.

It maintains the session’s transaction history and provides functionality
to retrieve or clear recorded actions as needed.
'''

class RecordActions:
    def __init__(self):
        self.transactions = []

    '''
    Records a standard banking transaction.

    Stores transaction details including transaction code,
    account holder name, account number, transaction amount,
    and any additional metadata.
    '''

    def record_transaction(self, code, name, account_num, amount, misc="N/A"):
        transaction = {
            'code': code,
            'name': name,
            'account_num': account_num,
            'amount': amount,
            'misc': misc
        }
        self.transactions.append(transaction)

    
    '''
    Records a transfer transaction between two accounts.

    Stores transaction details including sender account,
    receiver account, transfer amount, and any additional
    metadata.
    '''

    def record_transfer(self, code, account_num_sender, account_num_reciever, amount, misc="N/A", name="Standard_Account"):
        transaction = {
            'code': code,
            'name': name,
            'account_num':account_num_sender,
            'account_num_sender': account_num_sender,
            'account_num_reciever': account_num_reciever,
            'amount': amount,
            'misc': misc
        }
        self.transactions.append(transaction)


    '''
    Retrieves the list of recorded transactions for the current session.
    '''
    def get_transactions(self):
        return self.transactions

    '''
    Clears all recorded transactions for the current session.
    '''
    def clear_transactions(self):
        self.transactions = []
