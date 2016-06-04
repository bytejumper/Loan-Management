import Tkinter as tk
import tkMessageBox
import pandas as pd
import csv
from datetime import date
import account

class LoanManagement(tk.Tk):
    def __init__(self, parent, loans):
        '''create window
        '''
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.loans = loans
        self.frame1()
        self.frame2()
        self.frame3()
                
        
    def frame1(self):
        '''shows list of loans
        '''
        frame1 = tk.Frame(self.parent, relief = 'sunken',
            borderwidth = 2, padx = 2, pady = 2)
        frame1.pack(side = 'left', fill = 'y', expand = 1)
         
        mid = tk.Frame(frame1, borderwidth = 1, relief = 'groove')
        mid.pack(fill = 'y', expand = 1)
        self.loanlist = tk.Listbox(mid, borderwidth = 0, height = 8)
        self.loanlist.pack(side = 'left', fill = 'y', expand = 1)
        for i in range(len(self.loans)):
            self.insert_loan(self.loans[i])
        self.loanlist.bind('<<ListboxSelect>>', self.on_select)
        
        bottom = tk.Frame(frame1)
        bottom.pack(fill = 'x', expand = 1)
        self.delete = tk.Button(bottom, text = '-', command = self.delete_loan,
            state = 'disabled')
        self.delete.pack(side = 'right')
        self.add = tk.Button(bottom, text = '+', command = self.add_loan)
        self.add.pack(side = 'right')
        
        
    def frame2(self):
        '''shows loan details
        '''
        frame2 = tk.Frame(self, relief = 'sunken',
            borderwidth = 2, padx = 2, pady = 2)
        frame2.pack(side = 'left', fill = 'y', expand = 1)
        
        self.top = tk.Frame(frame2, borderwidth = 1, relief = 'groove')
        self.top.pack(fill = 'y', expand = 1)
        self.left = tk.Frame(self.top)
        self.left.pack(side = 'left', fill = 'y', expand = 1)
        label = tk.Label(self.left, text = 'Type \n' + 
            'Disbursement Date \n' +
            'Original Amount \n' +
            'Current Amount \n' +
            'APR \n' +
            'Monthly Payment \n' +
            'Extra Payment \n' +
            'As of', justify = 'right')
        label.pack()
        
        self.right = tk.Frame(self.top)
        self.right.pack(side = 'left', fill = 'y', expand = 1)
        self.loan_info = tk.StringVar()
        info = tk.Label(self.right, textvariable = self.loan_info, width = 30, 
            justify = 'left')
        info.pack()
        
        bottom = tk.Frame(frame2)
        bottom.pack(fill = 'x', expand = 1)
        self.edit = tk.Button(bottom, text = 'Edit', state = 'disabled',
            command = self.edit_loan)
        self.edit.pack(side = 'right')
        self.cancel = tk.Button(bottom, text = 'Cancel', state = 'disabled',
            command = self.reset)
        self.cancel.pack(side = 'right')
        
    
    def frame3(self):
        '''shows lifecycle information
        '''
        frame3 = tk.Frame(self, relief = 'sunken',
            borderwidth = 2, padx = 2, pady = 2)
        frame3.pack(side = 'left', fill = 'y', expand = 1)
        
        self.lifeVar = tk.StringVar()
        label = tk.Label(frame3, textvariable = self.lifeVar
        , wraplength = 200
        )
        label.pack(fill = 'x', expand = 1)
        
        self.pay = tk.Button(frame3, text = 'Payoff Time', state = 'disabled',
            command = self.check_payoff)
        self.pay.pack() 
        self.bal = tk.Button(frame3, text = 'Balance After', state = 'disabled',
            command = self.check_balance)
        self.bal.pack(side = 'left', fill = 'x', expand = 1)
        self.MonthVar = tk.IntVar()
        self.mth = tk.Entry(frame3, textvariable = self.MonthVar, width = 5, 
            bd = 2, justify = 'center', state = 'disabled')
        self.mth.pack(side = 'left')
        self.MonthVar.set(1)


    def insert_loan(self, loan, index = None):
        '''add loan to listbox
        '''
        if index is None:
            index = self.loanlist.size()
        self.loanlist.insert(index,
                getattr(loan, 'disburse_date') + '\t\t' +
                '${:9,.2f}'.format(getattr(loan, 'orig_bal')) + '\t\t' +
                str(getattr(loan, 'r')))
    
    
    def on_select(self, event):
        '''show loan information
        '''
        self.index = int(self.loanlist.curselection()[0])
        l = loans[self.index]
        self.loan_info.set(getattr(l, 'name') + '\n' +
            str(getattr(l, 'disburse_date')) + '\n' +
            '${:,.2f}'.format(getattr(l, 'orig_bal')) + '\n' +
            '${:,.2f}'.format(l.get_balance()) + '\n' +
            '{:2.2f}%'.format(getattr(l, 'r')) + '\n' +
            '${:,.2f}'.format(getattr(l, 'payment')) + '\n' +
            '${:,.2f}'.format(getattr(l,'extra_payment')) + '\n' +
            str(getattr(l, 'asof')))
        
        self.edit.config(state = 'normal')
        self.delete.config(state = 'normal')
        self.pay.config(state = 'normal')
        self.bal.config(state = 'normal')
        self.mth.config(state = 'normal')


    def reset(self):
        '''resets widgets to original states
        '''
        try:
            self.add_frame.forget()
        except:
            pass
        self.left.pack(side = 'left', fill = 'y', expand = 1)
        self.right.pack(side = 'left', fill = 'y', expand = 1)
        self.edit.config(text = 'Edit', command = self.edit_loan, state = 'disabled')
        self.cancel.config(state = 'disabled')
        self.lifeVar.set('')
        
    
    def add_loan(self):
        '''display entry widgets
        '''
        self.reset()
        self.right.forget()
        self.left.forget()
        self.add_frame = tk.Frame(self.top)
        self.add_frame.pack()
        self.TypeVar = tk.StringVar()
        self.eType = tk.Entry(self.add_frame, textvariable = self.TypeVar, 
            width = 30, bd = 0, justify = 'left')
        self.TypeVar.set('Type')
        self.eType.pack()
        self.DateVar = tk.StringVar()
        self.eDate = tk.Entry(self.add_frame, textvariable = self.DateVar,
            bd = 0, justify = 'left')
        self.DateVar.set('Disbursement Date')
        self.eDate.pack()
        self.OrigVar = tk.DoubleVar()
        self.eOrig = tk.Entry(self.add_frame, textvariable = self.OrigVar,
            bd = 0, justify = 'left')
        self.OrigVar.set('Original Balance')
        self.eOrig.pack()
        self.CurrVar = tk.DoubleVar()
        self.eCurr = tk.Entry(self.add_frame, textvariable = self.CurrVar,
            bd = 0, justify = 'left')
        self.CurrVar.set('Current Balance')
        self.eCurr.pack()
        self.AprVar = tk.DoubleVar()
        self.eApr = tk.Entry(self.add_frame, textvariable = self.AprVar,
            bd = 0, justify = 'left')
        self.AprVar.set('APR (percent)')
        self.eApr.pack()
        self.MonthPayVar = tk.DoubleVar()
        self.eMonthPay = tk.Entry(self.add_frame, textvariable = self.MonthPayVar,
            bd = 0, justify = 'left')
        self.MonthPayVar.set('Monthly Payment')
        self.eMonthPay.pack()
        self.ExtraPayVar = tk.DoubleVar()
        self.eExtraPay = tk.Entry(self.add_frame, textvariable = self.ExtraPayVar,
            bd = 0, justify = 'left')
        self.ExtraPayVar.set('Extra Payment')
        self.eExtraPay.pack()
        
        self.lifeVar.set('')
        ## TODO select all text in each Entry box upon activation
        self.edit.config(text = 'Save', command = self.save_add, state = 'normal')
        self.cancel.config(state = 'normal')
    
    
    def save_add(self):
        '''add loan to loan object list and listbox
        '''
        ## TODO error check to make sure all fields have appropriate value types
        loans.append(account.Loan(self.TypeVar.get(), self.DateVar.get(), 
            self.OrigVar.get(), self.AprVar.get(), self.MonthPayVar.get(),
            bal = self.CurrVar.get(), extra_payment = self.ExtraPayVar.get()))
        self.insert_loan(loans[-1]) 
        
        global edited
        edited = True
        
        self.reset()
        ## TODO select and display loan just added
        self.loanlist.activate(len(loans) - 1)
    
    
    def delete_loan(self):
        '''delete from loan object list and listbox
        '''
        self.loans.pop(self.index)
        self.loanlist.delete(self.index)
            
        global edited 
        edited = True 
        
        
    def edit_loan(self):
        '''display entry widgets
        '''
        l = loans[self.index]
        self.add_loan()
        self.TypeVar.set(getattr(l, 'name'))
        self.eType.config(state = 'disabled')
        self.DateVar.set(getattr(l, 'disburse_date'))
        self.eDate.config(state = 'disabled')
        self.OrigVar.set(getattr(l, 'orig_bal'))
        self.eOrig.config(state = 'disabled')
        self.CurrVar.set(l.get_balance())
        self.AprVar.set(getattr(l, 'r'))
        self.eApr.config(state = 'disabled')
        self.MonthPayVar.set(getattr(l, 'payment'))
        self.ExtraPayVar.set(getattr(l, 'extra_payment'))
        self.edit.config(command = self.save_edit)
        
        
    def save_edit(self):
        '''
        save values to data source
        set edited variable to True
        '''
        l = loans[self.index]
        
        l.edit(bal = self.CurrVar.get(), payment = self.MonthPayVar.get(), 
            extra_payment = self.ExtraPayVar.get(), date = date.today())
        
        global edited
        edited = True
        
        self.reset()
        
        
    def check_payoff(self):
        '''show years/months to payoff
        '''
        l = loans[self.index]
        ob = l.get_balance()
        op = getattr(l, 'payment')
        oe = getattr(l, 'extra_payment')
        try:
            l.edit(bal = self.CurrVar.get(), payment = self.MonthPayVar.get(), 
            extra_payment = self.ExtraPayVar.get())
        except:
            pass
        data = account.months_to_payoff(l)
        ## subtract one b/c original balance is included in list
        m = len(data[0]) - 1
        e = data[0][-1]
        i = sum(data[1])
        self.lifeVar.set(str(m) + ' months (' + 
            '{:2.2f}'.format(m/12.0) + ' years)\nExtra ' +
            '${:,.2f}'.format(abs(e)) + ' paid.\nPaying ' +
            '${:,.2f}'.format(i) + ' in interest.')
        l.edit(bal = ob, payment = op, extra_payment = oe)


    def check_balance(self):
        '''show balance after number of months
        '''
        l = loans[self.index]
        ob = l.get_balance()
        op = getattr(l, 'payment')
        oe = getattr(l, 'extra_payment')
        try:
            l.edit(bal = self.CurrVar.get(), payment = self.MonthPayVar.get(), 
            extra_payment = self.ExtraPayVar.get())
        except:
            pass
        m = self.MonthVar.get()
        data = account.balance_after(l, m)
        e = data[0][-1]
        i = sum(data[1])
        self.lifeVar.set('After ' + str(m) + ' months (' + 
            '{:2.2f}'.format(m/12.0) + ' years)\nRemaining balance is ' +
            '${:,.2f}'.format(e) + '.\nPaying ' +
            '${:,.2f}'.format(i) + ' in interest.')
        l.edit(bal = ob, payment = op, extra_payment = oe)

        
def on_closing():
    '''if changes made, ask to save
    '''
    global edited
    if edited == True:
        if tkMessageBox.askyesno('Save Changes', 
            "Changes made.  Do you want to save before quitting?"):
            ## sort debts by apr, original balance, and current balance (descending)
            loans.sort(key = 
                lambda x: (getattr(x, 'r'), 
                    getattr(x, 'orig_bal'), 
                    x.get_balance()), 
                reverse = True)
            ## save changes
            loans.sort(
                key = lambda x: 
                    (getattr(x, 'r'), getattr(x, 'orig_bal')), 
                reverse = True)
            d = {'apr': [], 'currBalance': [], 'currDate': [], 
                'disburseDate': [], 'name': [], 'origBalance': [], 
                'payment': [], 'extraPayment': []}
            for i in range(len(loans)):
                l = loans[i]
                d['apr'].append(getattr(l, 'r'))
                d['currBalance'].append(l.get_balance())
                d['currDate'].append(getattr(l, 'asof'))
                d['disburseDate'].append(getattr(l, 'disburse_date'))
                d['name'].append(getattr(l, 'name'))
                d['origBalance'].append(getattr(l, 'orig_bal'))
                d['payment'].append(getattr(l, 'payment'))
                d['extraPayment'].append(getattr(l, 'extra_payment'))
            debts = pd.DataFrame(d)
            debts.to_csv('debts.csv', index = False)
        app.destroy()   
    else:
        app.destroy()
        
if __name__ == '__main__':
    '''
    initiates application window; waits indefinitely for actions; 
    initialize global variables
    '''
    debts = pd.read_csv('debts.csv')
    loans = []
    for i in range(len(debts)):
        d = debts.values[i]
        loans.append(account.Loan(d[5], d[3], d[6], d[0], d[7], 
                bal = d[1], extra_payment = d[4], asof = d[2]))
    app = LoanManagement(None, loans)
    edited = False
    app.title('Loan Manager')
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()         
