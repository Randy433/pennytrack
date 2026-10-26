from flask import Flask, render_template
from pennytrack import load_transactions, calculate_financial_summary

app = Flask(__name__)


@app.route("/")
def home():
    transactions = load_transactions()
    summary = calculate_financial_summary(transactions)
    return render_template("index.html", transactions = transactions, summary = summary)


if __name__ == "__main__":
    app.run(debug=True)
