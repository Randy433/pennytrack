from flask import Flask, render_template
from pennytrack import load_transactions

app = Flask(__name__)


@app.route("/")
def home():
    transactions = load_transactions()
    return render_template("index.html", transactions = transactions)


if __name__ == "__main__":
    app.run(debug=True)
