'''
Object to hold a single instance of an account.

This object is an encapsulation of the attributes of a bank account
It is interacted with during methods as paying bills, withdrawing money, transfering money, depositing money

Stores the following information
    - Name
    - Account number
    - Balance
    - Status
    - Plan

'''
class Account:
    def __init__(self, name, accountNum, balance, status, plan):
        self.name = name
        self.accountNum = accountNum
        self.balance = balance
        self.status = status
        self.plan = plan