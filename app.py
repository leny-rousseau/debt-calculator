from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///debt-calculator.db'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_paid = db.Column(db.Float, nullable=False)
    payer = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

def calculate_balance():
    leny_total = db.session.query(db.func.sum(Transaction.amount_paid)).filter_by(payer='Leny').scalar() or 0
    cyril_total = db.session.query(db.func.sum(Transaction.amount_paid)).filter_by(payer='Cyril').scalar() or 0
    return leny_total, cyril_total

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        amount_paid = float(request.form['amount_paid'])
        payer = request.form['payer']
        description = request.form['description']

        transaction = Transaction(amount_paid=amount_paid, payer=payer, description=description)
        db.session.add(transaction)
        db.session.commit()

    leny_total, cyril_total = calculate_balance()
    if leny_total > cyril_total:
        balance_message = f"Cyril owes Leny {((leny_total - cyril_total) / 2):.2f} euros."
    elif cyril_total > leny_total:
        balance_message = f"Leny owes Cyril {((cyril_total - leny_total) / 2):.2f} euros."
    else:
        balance_message = "The balance is equal."

    transactions = Transaction.query.all()
    return render_template('index.html', transactions=transactions, balance_message=balance_message, leny_total=leny_total, cyril_total=cyril_total)

@app.route('/delete/<int:id>')
def delete_transaction(id):
    transaction = Transaction.query.get(id)
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)