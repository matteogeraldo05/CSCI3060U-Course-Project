# record transactions and transfers to write on logout
class RecordActions:
    def __init__(self):
        self.transactions = []

    def record_transaction(self, code, name, account_num, amount, misc="N/A"):
        transaction = {
            'code': code,
            'name': name,
            'account_num': account_num,
            'amount': amount,
            'misc': misc
        }
        self.transactions.append(transaction)

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

    def get_transactions(self):
        return self.transactions

    def clear_transactions(self):
        self.transactions = []
