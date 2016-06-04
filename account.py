from datetime import date


class Account(object):
    def __init__(self, name, bal, r, asof = date.today()):
        '''Create instance of account object
        
        name: name
        bal: current balance 
        r: annual interest rate as percentage
        asof: date the loan information is current
        '''
        self.name = name
        self.bal = bal
        self.r = r
        self.asof = asof
        
        
    def accrue_interest(self, t = 1):
        '''Add to balance one month's worth of interest
        
        return: amount of interest accrued
        '''        
        interest = self.bal * (self.r/100/12) * t
        self.bal += interest
        return interest
        
        
    def edit(self, bal, date = date.today()):
        '''Edit current balance of loan
        
        bal: current balance
        '''
	self.bal = bal
	self.asof = date
            
    
    def get_balance(self):
        '''Return current balance of loan
        
        return: bal
        '''
        return self.bal
            
        
class Loan(Account):
    def __init__(self, name, disburse_date, orig_bal, r, payment, 
                 bal = None, extra_payment = 0, asof = date.today()):
        '''Create instance of loan object
        
        name: name/description of loan
        disburseDate: date of disbursement; preferred format MM/DD/YYYY
        origBal: original balance
        apr: annual interest rate as percentage
        payment: monthly payment amount
        bal: current balance; defaults to origBal
        extraPayment: additional monthly payment amount; defaults to zero
        asof: date the loan information is current
        '''
        
        self.name = name
        self.disburse_date = disburse_date
        self.orig_bal = orig_bal
        self.r = r
        self.payment = payment
        if bal is None:
            self.bal = orig_bal
	else:
            self.bal = bal
        self.extra_payment = extra_payment
        self.asof = asof
        
        
    def edit(self, payment = None, 
            bal = None, extra_payment = None, date = date.today()):
        '''Edit payment or current balance of loan
        
        payment: monthly payment amount
        bal: current balance
        extraPayment: additional monthly payment amount
        '''
        if payment is not None:
            self.payment = payment
        if bal is not None:
	        self.bal = bal
	if extra_payment is not None:
	        self.extra_payment = extra_payment
	self.asof = date


    def make_payment(self, payment = None, extra_payment = None):
        '''Determine the new balance after one monthly payment
        
        payment: payment amount
        extraPayment: additional payment amount
        return: total interest accrued
        '''
        if payment is None:
            payment = self.payment
        if extra_payment is None:
            extra_payment = self.extra_payment
        ia = 0
        ia += self.accrue_interest()
        self.bal -= payment
        self.bal -= extra_payment
        #for p in [extra_payment, payment]:   
        #    ia += self.accrue_interest(0.5)
        #    self.bal -= p
        return ia
        
        
def months_to_payoff(Loan):
    '''Calculate the number of months to payoff when making regular payments 

    Loan: object of Loan class
    
    returns: number of months to payoff, excess paid from full payment in last month
    '''
    balance = [Loan.get_balance()]
    interest = [0]
    while Loan.get_balance() > 0:
        interest.append(Loan.make_payment())
        balance.append(Loan.get_balance())
    Loan.edit(bal = balance[0])
    return balance, interest


def balance_after(Loan, c):
    '''Find balance after set number of months
    
    Loan: object of Loan class
    c: number of months of payments
    
    return: balance after c months of payments
    '''
    balance = [Loan.get_balance()]
    interest = [0]
    for i in range(c):
        interest.append(Loan.make_payment())
        balance.append(Loan.get_balance())
    Loan.edit(bal = balance[0])
    return balance, interest


#import pylab 
# 
#for i in [0, 80]:
#    l1 = Loan('Test loan', '5/12/07', 24099.76, 7.65, 196.29, extra_payment = i)
#    r = months_to_payoff(l1)
#    pylab.figure(1)
#    pylab.plot(r[0])
#    pylab.figure(2)
#    pylab.plot(r[1])
#pylab.figure(1)
#pylab.title('Balance by Month')
#pylab.xlabel('Month')
#pylab.ylabel('Amount')
#pylab.figure(2)
#pylab.title('Interest by Month')
#pylab.xlabel('Month')
#pylab.ylabel('Amount')
#pylab.show()


import pandas as pd

debts = pd.read_csv('debts.csv')
loans = []
#for i in range(len(debts)):
for i in [6,7,15,16]:
    d = debts.values[i]
    loans.append(Loan(d[4], d[3], d[6], d[0], d[5], 
            bal = d[1], extra_payment = d[7], asof = d[2]))
            
#balance = [Loan.get_balance()]
#interest = [0]
#while Loan.get_balance() > 0:
#    interest.append(Loan.make_payment())
#    balance.append(Loan.get_balance())
#Loan.edit(bal = balance[0])

#import itertools
#for subset in itertools.permutations(loans):
#    for m in range(60):
#        for l in subset:
#        
#        l.make_payment(extra_payment = l.extra_payment + 1275)
#        r = months_to_payoff(l)