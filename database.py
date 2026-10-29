import sqlite3


def create_connection():
    connection = sqlite3.connect("pennytrack.db")
    return connection


def create_transactions_table():
    connection = create_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_transaction(amount, transaction_type, category, description):
    connection = create_connection()
    connection.execute(
        """
       INSERT INTO transactions(amount, type, category, description)
       VALUES(?, ?, ?, ?)
       """,
        (amount, transaction_type, category, description)
    )
    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_transactions_table()
    add_transaction(
        1500,
        "expense",
        "Food",
        "Lunch"
    )
    print("Transactions table created successfully!")
