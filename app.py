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
        transactions = load_transactions()
        summary = calculate_financial_summary(transactions)
        
        return render_template(
            "index.html",
            transactions=transactions,
            summary=summary,
            error=str(error),
            form_data=request.form
        ), 400

    transactions = load_transactions()
    transactions.append(transaction)
    save_transactions(transactions)

    return redirect(url_for("home"))

@app.route("/edit-transaction/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction_web(transaction_id):
    transactions = load_transactions()
    
    if transaction_id >= len(transactions):
        return "Transaction not found.", 404
    
    transaction = transactions[transaction_id]
    
    if request.method == "POST":
        amount = request.form.get("amount", "")
        transaction_type = request.form.get("type", "")
        category = request.form.get("category", "")
        description = request.form.get("description", "")
        
        try:
            updated_transaction = create_transaction(
                amount,
                transaction_type,
                category,
                description
            )
        except ValueError as error:
            return render_template(
                "edit_transaction.html",
                transaction=transaction,
                error=str(error),
                form_data=request.form
            ), 400
        
        transactions[transaction_id] = updated_transaction
        save_transactions(transactions)
        return redirect(url_for("home"))
    return render_template("edit_transaction.html", transaction=transaction)

@app.route("/delete-transaction/<int:transaction_id>", methods=["POST"])
def delete_transaction_web(transaction_id):
    transactions = load_transactions()
    
    if transaction_id >= len(transactions):
        return "Transaction not found", 404
    
    transactions.pop(transaction_id)
    save_transactions(transactions)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
