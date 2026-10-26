from flask import Flask, render_template, request, redirect, url_for
from pennytrack import (
    load_transactions,
    save_transactions,
    calculate_financial_summary,
    create_transaction
    )

app = Flask(__name__)


@app.route("/")
def home():
    transactions = load_transactions()
    summary = calculate_financial_summary(transactions)
    return render_template("index.html", transactions=transactions, summary=summary)


@app.route("/add-transaction", methods=["POST"])
def add_transaction_web():
    amount = request.form.get("amount", "")
    transaction_type = request.form.get("type", "")
    category = request.form.get("category", "")
    description = request.form.get("description", "")

    try:
        transaction = create_transaction(amount, transaction_type, category, description)
    except ValueError as error:
        return str(error), 400

    transactions = load_transactions()
    transactions.append(transaction)
    save_transactions(transactions)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
