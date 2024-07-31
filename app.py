from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount_paid = float(request.form['amount_paid'])
        payer = request.form['payer']

        amount_owe = amount_paid / 2

        if payer == 'me':
            message = f"Your friend owes you {amount_owe} euros."

        else:
            message = f"You owe your friend {amount_owe} euros."

        return render_template('index.html', message=message)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)