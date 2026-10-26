import json
import os
import tempfile
import unittest
import app as web_app
from pennytrack import create_transaction
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

        user_inputs = ["1", "7000", "income", "Business", "Web development"]

        with patch("builtins.input", side_effect=user_inputs), \
                patch("pennytrack.save_transactions"):
            edit_transaction(transactions)

        self.assertEqual(transactions[0]["amount"], 7000)
        self.assertEqual(transactions[0]["type"], "income")
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


class TestPennyTrackWeb(unittest.TestCase):

    def setUp(self):
        self.client = web_app.app.test_client()

    def test_homepage_loads(self):
        with patch("app.load_transactions", return_value=[]):
            response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"PennyTrack", response.data)

    def test_add_transaction_web(self):
        with patch("app.load_transactions", return_value=[]), \
                patch("app.save_transactions") as mock_save:

            response = self.client.post(
                "/add-transaction",
                data={
                    "amount": "5000",
                    "type": "income",
                    "category": "Salary",
                    "description": "Monthly salary"
                }
            )

        self.assertEqual(response.status_code, 302)

        saved_transactions = mock_save.call_args[0][0]

        self.assertEqual(len(saved_transactions), 1)
        self.assertEqual(saved_transactions[0]["amount"], 5000.0)
        self.assertEqual(saved_transactions[0]["type"], "income")

    def test_add_invalid_transaction_web(self):
        with patch("app.load_transactions", return_value=[]), \
                patch("app.save_transactions") as mock_save:

            response = self.client.post(
                "/add-transaction",
                data={
                    "amount": "-500",
                    "type": "expense",
                    "category": "Food",
                    "description": "Invalid expense"
                }
            )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Amount must be greater than zero", response.data)
        mock_save.assert_not_called()

    def test_delete_transaction_web(self):
        transactions = [
            {
                "amount": 5000,
                "type": "income",
                "category": "Salary",
                "description": "Monthly salary"
            }
        ]

        with patch("app.load_transactions", return_value=transactions), \
                patch("app.save_transactions") as mock_save:

            response = self.client.post("/delete-transaction/0")

        self.assertEqual(response.status_code, 302)

        saved_transactions = mock_save.call_args[0][0]
        self.assertEqual(saved_transactions, [])

    def test_edit_transaction_web(self):
        transactions = [
            {
                "amount": 5000,
                "type": "income",
                "category": "Salary",
                "description": "Old salary"
            }
        ]

        with patch("app.load_transactions", return_value=transactions), \
                patch("app.save_transactions") as mock_save:

            response = self.client.post(
                "/edit-transaction/0",
                data={
                    "amount": "7000",
                    "type": "income",
                    "category": "Business",
                    "description": "Web development"
                }
            )

        self.assertEqual(response.status_code, 302)

        saved_transactions = mock_save.call_args[0][0]

        self.assertEqual(saved_transactions[0]["amount"], 7000.0)
        self.assertEqual(saved_transactions[0]["category"], "Business")
        self.assertEqual(
            saved_transactions[0]["description"],
            "Web development"
        )


if __name__ == "__main__":
    unittest.main()
