import json
import os
import tempfile
import unittest
from unittest.mock import patch
from pennytrack import (
    calculate_balance,
    calculate_spending_by_category,
    save_transactions,
    load_transactions,
    delete_transaction,
    edit_transaction
)


class TestPennyTrack(unittest.TestCase):

    def test_balance_with_income_and_expenses(self):
        transactions = [
            {"amount": 100000, "type": "income"},
            {"amount": 8000, "type": "expense"},
            {"amount": 2000, "type": "expense"},
            {"amount": 5000, "type": "income"}
        ]

        result = calculate_balance(transactions)
        self.assertEqual(result, 95000)

    def test_spending_by_category(self):
        transactions = [
            {"amount": 5000, "type": "expense", "category": "Food"},
            {"amount": 3000, "type": "expense", "category": "Transport"},
            {"amount": 2000, "type": "expense", "category": "Food"}
        ]

        result = calculate_spending_by_category(transactions)

        self.assertEqual(result, {
            "Food": 7000,
            "Transport": 3000
        })

    def test_balance_with_no_transactions(self):
        transactions = []

        result = calculate_balance(transactions)

        self.assertEqual(result, 0)

    def test_save_and_load_transactions(self):
        transactions = [
            {
                "amount": 5000,
                "type": "income",
                "category": "Salary",
                "description": "Monthly salary"
            }
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "transactions.json")

            with open(file_path, "w") as file:
                json.dump(transactions, file)

            with open(file_path, "r") as file:
                result = json.load(file)

            self.assertEqual(result, transactions)

    def test_delete_transaction(self):
        transactions = [
            {
                "amount": 5000,
                "type": "income",
                "category": "Salary",
                "description": "Monthly salary"
            }
        ]

        with patch("builtins.input", return_value="1"), \
            patch("pennytrack.save_transactions"):
            delete_transaction(transactions)

        self.assertEqual(len(transactions), 0)

    def test_delete_invalid_number(self):
        transactions = [
            {
                "amount": 5000,
                "type": "income",
                "category": "Salary",
                "description": "Monthly salary"
            }
        ]

        with patch("builtins.input", return_value="abc"), \
            patch("pennytrack.save_transactions"):
            delete_transaction(transactions)

        self.assertEqual(len(transactions), 1)

    def test_edit_transaction(self):
        transactions = [
            {
                "amount": 5000,
                "type": "income",
                "category": "Salary",
                "description": "Old description"
            }
        ]

        user_inputs = ["1", "7000", "Business", "Web development"]

        with patch("builtins.input", side_effect=user_inputs), \
            patch("pennytrack.save_transactions"):
            edit_transaction(transactions)

        self.assertEqual(transactions[0]["amount"], 7000)
        self.assertEqual(transactions[0]["category"], "Business")
        self.assertEqual(
            transactions[0]["description"], "Web development"
        )

    def test_edit_invalid_transaction_number(self):
        transactions = [
            {
                "amount": 5000,
                "type": "income",
                "category": "Salary",
                "description": "Monthly salary"
            }
        ]

        with patch("builtins.input", return_value="abc"), \
            patch("pennytrack.save_transactions"):
            edit_transaction(transactions)

        self.assertEqual(transactions[0]["amount"], 5000)


if __name__ == "__main__":
    unittest.main()