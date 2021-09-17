import numpy as np


# Evaluate performance.

def read_ledger(ledger_file='ledger.txt'):
    '''
    Reads and reports useful information from ledger_file.
    '''
    
    def read_transaction(s):
        transaction_type, date, stock, number_of_shares, price, amount_spent_earned = s.split(',')
        date, stock, number_of_shares = map(int, [date, stock, number_of_shares])
        price, amount_spent_earned = map(float, [price, amount_spent_earned])
        return transaction_type, date, stock, number_of_shares, price, amount_spent_earned
    
    # (f'{transaction_type},{date},{stock},{number_of_shares},{price:.2f},{amount_spent_earned:.2f}\n')
    with open(ledger_file) as f:
        transactions = f.readlines()
    
    transactions = [*map(read_transaction, transactions)]
    
    total_spent = sum([t[5] for t in transactions if t[0] == 'buy' and not np.isnan(t[5])])
    total_earned = sum([t[5] for t in transactions if t[0] == 'sell' and not np.isnan(t[5])])
    total_amount = sum([t[5] for t in transactions if not np.isnan(t[5])])
    
    return {
        'total_spent': total_spent,
        'total_earned': total_earned,
        'total_amount': total_amount
    }