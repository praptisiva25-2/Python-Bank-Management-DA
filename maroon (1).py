import tkinter as tk
from tkinter import messagebox
import pickle
import os
import re

class Account:
    def __init__(self):
        self.accNo = 0
        self.name = ''
        self.deposit = 0
        self.type = ''
        self.password = ''

    def createAccount(self, accNo, name, account_type, deposit, password):
        self.accNo = accNo
        self.name = name
        self.type = account_type
        self.deposit = deposit
        self.password = password

def writeAccount(accNo, name, account_type, deposit, password):
    account = Account()
    account.createAccount(accNo, name, account_type, deposit, password)
    writeAccountsFile(account)

def writeAccountsFile(account):
    file_path = "accounts.data"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as infile:
            oldlist = pickle.load(infile)
        oldlist.append(account)
    else:
        oldlist = [account]

    with open(file_path, 'wb') as outfile:
        pickle.dump(oldlist, outfile)
    messagebox.showinfo("Saved", "Your account is created")

def displayAll():
    file_path = "accounts.data"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as infile:
            mylist = pickle.load(infile)
        for item in mylist:
            print(item.accNo, " ", item.name, " ", item.type, " ", item.deposit)
    else:
        print("No records to display")

def is_valid_accNo(accNo):
    file_path = "accounts.data"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as infile:
            mylist = pickle.load(infile)
            for item in mylist:
                if item.accNo == accNo:
                    return False
    return True

def is_valid_password(password):
    # Password must be at least 6 characters, alphanumeric, with at least one capital and one special character
    if len(password) < 6:
        return False
    if not re.match(r'^(?=.*[A-Z])(?=.*[!@#$%^&*()_+=\[{\]};:<>|./?,-])(?=.*[0-9a-zA-Z]).*$', password):
        return False
    return True

def is_valid_password_and_accNo(accNo, password):
    file_path = "accounts.data"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as infile:
            mylist = pickle.load(infile)
            for item in mylist:
                if item.accNo == accNo and item.password == password:
                    return True
    return False

def depositAndWithdraw(num1, num2, amount):
    file_path = "accounts.data"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as infile:
            mylist = pickle.load(infile)

        for item in mylist:
            if item.accNo == num1:
                if num2 == 1:
                    item.deposit += amount
                    messagebox.showinfo("updated", "Your account is updated")
                elif num2 == 2:
                    if (item.deposit - amount) >= 5000:  # Minimum balance requirement
                        item.deposit -= amount
                        messagebox.showinfo("updated", "Your account is updated")
                    else:
                        print("You cannot withdraw this amount, minimum balance requirement not met.")

        with open(file_path, 'wb') as outfile:
            pickle.dump(mylist, outfile)
    else:
        print("No records to update")

def displaySp(num):
    file_path = "accounts.data"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as infile:
            mylist = pickle.load(infile)
        found = False
        for item in mylist:
            if item.accNo == num:
                messagebox.showinfo("Balance Info","Your account Balance is Rs."+str(item.deposit))
                found = True
    else:
        print("No records to search")
    if not found:
        print("No existing record with this number")

def deleteAccount(num):
    file_path = "accounts.data"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as infile:
            oldlist = pickle.load(infile)
        newlist = [item for item in oldlist if item.accNo != num]
        with open(file_path, 'wb') as outfile:
            pickle.dump(newlist, outfile)
    else:
        print("No records to delete")

def modifyAccount(num, name, account_type, deposit):
    file_path = "accounts.data"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as infile:
            oldlist = pickle.load(infile)

        for item in oldlist:
            if item.accNo == num:
                item.name = name
                item.type = account_type
                item.deposit = deposit

        with open(file_path, 'wb') as outfile:
            pickle.dump(oldlist, outfile)
    else:
        print("No records to modify")

def create_account_window():
    account_window = tk.Toplevel()
    account_window.title("Create Account")

    tk.Label(account_window, text="Account Number:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(account_window, text="Account Holder Name:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(account_window, text="Account Type:").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(account_window, text="Initial Deposit:").grid(row=3, column=0, padx=10, pady=5)
    tk.Label(account_window, text="Password:").grid(row=4, column=0, padx=10, pady=5)

    accNo_entry = tk.Entry(account_window)
    name_entry = tk.Entry(account_window)
    deposit_entry = tk.Entry(account_window)
    password_entry = tk.Entry(account_window, show="*")

    accNo_entry.grid(row=0, column=1, padx=10, pady=5)
    name_entry.grid(row=1, column=1, padx=10, pady=5)
    deposit_entry.grid(row=3, column=1, padx=10, pady=5)
    password_entry.grid(row=4, column=1, padx=10, pady=5)

    account_types = ["Current", "Savings"]
    account_type_var = tk.StringVar(account_window)
    account_type_var.set(account_types[0])  # Default value

    account_type_dropdown = tk.OptionMenu(account_window, account_type_var, *account_types)
    account_type_dropdown.grid(row=2, column=1, padx=10, pady=5)

    def save_account():
        accNo = int(accNo_entry.get())
        name = name_entry.get()
        account_type = account_type_var.get()[0]  # Extracting the first character (C or S)
        deposit = int(deposit_entry.get())
        password = password_entry.get()
        
        if len(str(accNo)) != 12:
            messagebox.showerror("Error", "Account number must be 12 digits.")
            return

        if not is_valid_accNo(accNo):
            messagebox.showerror("Error", "Account number already exists.")
            return

        if deposit < 5000:
            messagebox.showerror("Error", "Initial deposit must be at least 5000.")
            return

        if not is_valid_password(password):
            messagebox.showerror("Error", "Password must be at least 6 characters, alphanumeric, with at least one capital and one special character.")
            return

        writeAccount(accNo, name, account_type, deposit, password)
        account_window.destroy()

    tk.Button(account_window, text="Save", command=save_account).grid(row=5, column=1, pady=10)

def deposit_window():
    deposit_window = tk.Toplevel()
    deposit_window.title("Deposit Amount")

    tk.Label(deposit_window, text="Account Number:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(deposit_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(deposit_window, text="Amount to Deposit:").grid(row=2, column=0, padx=10, pady=5)

    accNo_entry = tk.Entry(deposit_window)
    password_entry = tk.Entry(deposit_window, show="*")
    amount_entry = tk.Entry(deposit_window)

    accNo_entry.grid(row=0, column=1, padx=10, pady=5)
    password_entry.grid(row=1, column=1, padx=10, pady=5)
    amount_entry.grid(row=2, column=1, padx=10, pady=5)

    def deposit_amount():
        accNo = int(accNo_entry.get())
        password = password_entry.get()
        amount = int(amount_entry.get())
        if is_valid_password_and_accNo(accNo, password):
            depositAndWithdraw(accNo, 1, amount)
            deposit_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid account number or password.")

    tk.Button(deposit_window, text="Deposit", command=deposit_amount).grid(row=3, column=1, pady=10)

def withdraw_window():
    withdraw_window = tk.Toplevel()
    withdraw_window.title("Withdraw Amount")

    tk.Label(withdraw_window, text="Account Number:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(withdraw_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(withdraw_window, text="Amount to Withdraw:").grid(row=2, column=0, padx=10, pady=5)

    accNo_entry = tk.Entry(withdraw_window)
    password_entry = tk.Entry(withdraw_window, show="*")
    amount_entry = tk.Entry(withdraw_window)

    accNo_entry.grid(row=0, column=1, padx=10, pady=5)
    password_entry.grid(row=1, column=1, padx=10, pady=5)
    amount_entry.grid(row=2, column=1, padx=10, pady=5)

    def withdraw_amount():
        accNo = int(accNo_entry.get())
        password = password_entry.get()
        amount = int(amount_entry.get())
        if is_valid_password_and_accNo(accNo, password):
            depositAndWithdraw(accNo, 2, amount)
            withdraw_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid account number or password.")

    tk.Button(withdraw_window, text="Withdraw", command=withdraw_amount).grid(row=3, column=1, pady=10)

def balance_inquiry_window():
    balance_inquiry_window = tk.Toplevel()
    balance_inquiry_window.title("Balance Inquiry")

    tk.Label(balance_inquiry_window, text="Account Number:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(balance_inquiry_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)

    accNo_entry = tk.Entry(balance_inquiry_window)
    password_entry = tk.Entry(balance_inquiry_window, show="*")

    accNo_entry.grid(row=0, column=1, padx=10, pady=5)
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    def check_balance():
        accNo = int(accNo_entry.get())
        password = password_entry.get()
        if is_valid_password_and_accNo(accNo, password):
            displaySp(accNo)
            balance_inquiry_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid account number or password.")

    tk.Button(balance_inquiry_window, text="Check Balance", command=check_balance).grid(row=2, column=1, pady=10)

def close_account_window():
    close_account_window = tk.Toplevel()
    close_account_window.title("Close Account")

    tk.Label(close_account_window, text="Account Number:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(close_account_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)

    accNo_entry = tk.Entry(close_account_window)
    password_entry = tk.Entry(close_account_window, show="*")

    accNo_entry.grid(row=0, column=1, padx=10, pady=5)
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    def close_account():
        accNo = int(accNo_entry.get())
        password = password_entry.get()
        if is_valid_password_and_accNo(accNo, password):
            deleteAccount(accNo)
            close_account_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid account number or password.")

    tk.Button(close_account_window, text="Close Account", command=close_account).grid(row=2, column=1, pady=10)

def modify_account_window():
    modify_account_window = tk.Toplevel()
    modify_account_window.title("Modify Account")

    tk.Label(modify_account_window, text="Account Number:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(modify_account_window, text="New Name:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(modify_account_window, text="New Account Type:").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(modify_account_window, text="New Deposit:").grid(row=3, column=0, padx=10, pady=5)
    tk.Label(modify_account_window, text="Password:").grid(row=4, column=0, padx=10, pady=5)

    accNo_entry = tk.Entry(modify_account_window)
    name_entry = tk.Entry(modify_account_window)
    deposit_entry = tk.Entry(modify_account_window)
    password_entry = tk.Entry(modify_account_window, show="*")

    accNo_entry.grid(row=0, column=1, padx=10, pady=5)
    name_entry.grid(row=1, column=1, padx=10, pady=5)
    deposit_entry.grid(row=3, column=1, padx=10, pady=5)
    password_entry.grid(row=4, column=1, padx=10, pady=5)

    account_types = ["Current", "Savings"]
    account_type_var = tk.StringVar(modify_account_window)
    account_type_var.set(account_types[0])  # Default value

    account_type_dropdown = tk.OptionMenu(modify_account_window, account_type_var, *account_types)
    account_type_dropdown.grid(row=2, column=1, padx=10, pady=5)

    def modify_account():
        accNo = int(accNo_entry.get())
        name = name_entry.get()
        account_type = account_type_var.get()[0]  # Extracting the first character (C or S)
        deposit = int(deposit_entry.get())
        password = password_entry.get()
        if is_valid_password_and_accNo(accNo, password):
            modifyAccount(accNo, name, account_type, deposit)
            modify_account_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid account number or password.")

    tk.Button(modify_account_window, text="Modify Account", command=modify_account).grid(row=5, column=1, pady=10)

def money_transfer_window():
    transfer_window = tk.Toplevel()
    transfer_window.title("Money Transfer")

    tk.Label(transfer_window, text="Sender's Account Number:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(transfer_window, text="Receiver's Account Number:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(transfer_window, text="Amount to Transfer:").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(transfer_window, text="Password:").grid(row=3, column=0, padx=10, pady=5)

    sender_accNo_entry = tk.Entry(transfer_window)
    receiver_accNo_entry = tk.Entry(transfer_window)
    amount_entry = tk.Entry(transfer_window)
    password_entry = tk.Entry(transfer_window, show="*")

    sender_accNo_entry.grid(row=0, column=1, padx=10, pady=5)
    receiver_accNo_entry.grid(row=1, column=1, padx=10, pady=5)
    amount_entry.grid(row=2, column=1, padx=10, pady=5)
    password_entry.grid(row=3, column=1, padx=10, pady=5)

    def transfer_money():
        sender_accNo = int(sender_accNo_entry.get())
        receiver_accNo = int(receiver_accNo_entry.get())
        amount = int(amount_entry.get())
        password = password_entry.get()

        if is_valid_password_and_accNo(sender_accNo, password):
            depositAndWithdraw(sender_accNo, 2, amount)  # Withdraw from sender's account
            depositAndWithdraw(receiver_accNo, 1, amount)  # Deposit to receiver's account
            transfer_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid account number or password.")

    tk.Button(transfer_window, text="Transfer", command=transfer_money).grid(row=4, column=1, pady=10)
    
def intro():
    intro_label = tk.Label(root, text="BANK MANAGEMENT SYSTEM", font=("Helvetica", 16))
    intro_label.pack(pady=20)

root = tk.Tk()
root.title("Bank Management System")
root.configure(bg="#a1c5ff",padx=50,pady=80)

intro()

button_frame = tk.Frame(root, bg="#a1c5ff")
button_frame.pack()

create_account_btn = tk.Button(button_frame, text="New Account", command=create_account_window)
create_account_btn.grid(row=0, column=2, padx=10, pady=10)

deposit_btn = tk.Button(button_frame, text="Deposit Amount", command=deposit_window)
deposit_btn.grid(row=1, column=2, padx=10, pady=10)

withdraw_btn = tk.Button(button_frame, text="Withdraw Amount", command=withdraw_window)
withdraw_btn.grid(row=2, column=2, padx=10, pady=10)

transfer_btn = tk.Button(button_frame, text="Transfer Money", command=money_transfer_window)
transfer_btn.grid(row=6, column=2, padx=10, pady=10)

balance_btn = tk.Button(button_frame, text="Balance Enquiry", command=balance_inquiry_window)
balance_btn.grid(row=3, column=2, padx=10, pady=10)

close_account_btn = tk.Button(button_frame, text="Close an Account", command=close_account_window)
close_account_btn.grid(row=4, column=2, padx=10, pady=10)

modify_account_btn = tk.Button(button_frame, text="Modify an Account", command=modify_account_window)
modify_account_btn.grid(row=5, column=2, padx=10, pady=10)

exit_btn = tk.Button(button_frame, text="Exit", command=root.destroy)  
exit_btn.grid(row=7, column=2, padx=10, pady=10)

root.mainloop()
