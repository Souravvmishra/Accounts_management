from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure random key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define a Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    amount = db.Column(db.Float)
    transaction_type = db.Column(db.String(10))
    date = db.Column(db.String(10))

@app.route('/')
def index():
    transactions = Transaction.query.all()
    total_income = sum(transaction.amount for transaction in transactions if transaction.transaction_type == "income")
    total_expense = sum(transaction.amount for transaction in transactions if transaction.transaction_type == "expense")
    balance = total_income - total_expense
    return render_template('index.html', transactions=transactions, total_income=total_income, total_expense=total_expense, balance=balance)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    description = request.form['description']
    amount = float(request.form['amount'])
    transaction_type = request.form['transaction_type']
    date = request.form['date']

    transaction = Transaction(description=description, amount=amount, transaction_type=transaction_type, date=date)
    db.session.add(transaction)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
