from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

accounts = {}  # Dictionary to store account details

def generate_account_number():
    """Generates a random 10-digit account number."""
    return random.randint(1000000000, 9999999999)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['name']
        account_number = generate_account_number()
        accounts[account_number] = {'name': name, 'balance': 0.0}

        return render_template('success.html', 
                               message="Account created successfully!", 
                               account_number=account_number)
    return render_template('create_account.html')

@app.route('/view_account', methods=['GET', 'POST'])
def view_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        if account_number in accounts:
            account_details = accounts[account_number]
            return render_template('account_details.html', 
                                   name=account_details['name'], 
                                   account_number=account_number, 
                                   balance=account_details['balance'])
        else:
            return render_template('error.html', message="Account not found.")
    return render_template('view_account.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])

        if account_number in accounts:
            accounts[account_number]['balance'] += amount
            return render_template('success.html', message="Deposit successful!")
        else:
            return render_template('error.html', message="Account not found.")
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])
        min_balance = 500.0  # Set minimum balance

        if account_number in accounts:
            if accounts[account_number]['balance'] - amount >= min_balance:
                accounts[account_number]['balance'] -= amount
                return render_template('success.html', message="Withdrawal successful!")
            else:
                return render_template('error.html', message="Insufficient balance.")
        else:
            return render_template('error.html', message="Account not found.")
    return render_template('withdraw.html')

if __name__ == '__main__':
    app.run(debug=True)