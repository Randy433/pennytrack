import json

transactions = []


def add_transaction(transactions):
    while True:
        try:
            amount = float(input("Enter your amount: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
        except ValueError:
            print("Invalid Input, Enter a valid number")
            continue
        else:
            break
    while True:
        transaction_type = input("Enter type 'income' / 'expense: ").lower()
        if transaction_type == "income" or transaction_type == "expense":
            break
        print("Invalid type. Enter 'income' or 'expense'")
    category = input("Enter the category: ")
    description = input("Enter the description: ")

    transaction = {
        "amount": amount,
        "type": transaction_type,
        "category": category,
        "description": description,
    }

    transactions.append(transaction)
    save_transactions(transactions)
    print("Transactions Added Successfully!")


def create_transaction(amount, transaction_type, category, description):
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        raise ValueError("Amount must be a valid number.")
    if amount <= 0:
        raise ValueError("Amount must be a valid number.")
    transaction_type = transaction_type.strip().lower()
    if transaction_type not in ("income", "expense"):
        raise ValueError("Type must be income or expense.")
    if not category.strip():
        raise ValueError("Category cannot be empty.")
        
    transaction = {
        "amount": amount,
        "type": transaction_type,
        "category": category,
        "description": description,
    }

    return transaction


def view_transaction(transactions):
    if not transactions:
        print("No transactions found.")
        return

    print("\n========== ALL TRANSACTIONS ==========")

    for number, transaction in enumerate(transactions, start=1):
        amount = transaction["amount"]
        transaction_type = transaction.get("type", "unknown")
        category = transaction["category"]
        description = transaction["description"]

        print(f"{number}. {transaction_type.title()} | "
              f"₦{amount:,.2f} | {category} | {description}")


def calculate_balance(transactions):
    total_income = 0
    total_expenses = 0
    for transaction in transactions:
        if transaction.get('type') == 'income':
            total_income += transaction['amount']
        elif transaction.get('type')  == 'expense':
            total_expenses += transaction['amount']

    return total_income - total_expenses


def display_balance(transactions):
    balance = calculate_balance(transactions)

    print("\n===== Account Balance =====")
    print(f"Remaining balance: {balance:,.2f}")


def calculate_spending_by_category(transactions):
    category_total = {}
    for transaction in transactions:
        category = transaction['category']

        if category in category_total:
            category_total[category] += transaction['amount']
        else:
            category_total[category] = transaction['amount']
    return category_total


def display_financial_summary(transactions):
    total_income = 0
    total_expenses = 0
    for transaction in transactions:
        if transaction.get('type') == 'income':
            total_income += transaction['amount']
        elif transaction.get('type')  == 'expense':
            total_expenses += transaction['amount']
    balance = total_income - total_expenses
    print("========== PENNYTRACK SUMMARY ==========")
    print(f"Total Income:\t\t {total_income:,.2f}")
    print(f"Total Expenses:\t\t {total_expenses:,.2f}") 
    print(f"Remaining Balance:\t {balance:,.2f}")
    print("=======================================")


def calculate_financial_summary(transactions):
    total_income = 0
    total_expenses = 0

    for transaction in transactions:
        if transaction["type"] == "income":
            total_income += transaction["amount"]
        elif transaction["type"] == "expense":
            total_expenses += transaction["amount"]

    balance = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance
    }


def display_spending_by_category(category_total):
    print("\n===== SPENDING BY CATEGORY =====")
    if not category_total:
        print("No transactions found")
        return
    for category, total in category_total.items():
        print(f"{category}: ₦{total:,.2f}")


def spending_by_category(transactions):
    category_total = calculate_spending_by_category(transactions)
    display_spending_by_category(category_total)


def edit_transaction(transactions):
    if len(transactions) == 0:
        print("No transactions to edit.")
        return

    view_transaction(transactions)

    try:
        number = int(input("Which transaction do you want to edit? "))
        if number <= 0:
            print("Number must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid transaction number.")
        return

    index = number - 1

    if index >= len(transactions):
        print("Invalid transaction number.")
        return

    transaction = transactions[index]

    while True:
        try:
            amount = float(input("Enter new amount: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
        except ValueError:
            print("Invalid amount. Enter a valid number.")
            continue
        else:
            break
    while True:
        transaction_type = input("Enter type 'income' / 'expense: ").lower()
        if transaction_type == "income" or transaction_type == "expense":
            break
            print("Invalid type. Enter 'income' or 'expense'")
    transaction["amount"] = amount
    transaction["type"] = transaction_type
    transaction["category"] = input("Enter new category: ")
    transaction["description"] = input("Enter new description: ")

    save_transactions(transactions)
    print("Transaction updated successfully!")


def delete_transaction(transactions):
    if len(transactions) == 0:
        print("The transaction list is empty.")
        return

    view_transaction(transactions)

    try:
        number = int(input("Which transaction do you want to delete? "))
    except ValueError:
        print("Please enter a valid transaction number.")
        return

    if number < 1 or number > len(transactions):
        print("Invalid transaction number.")
        return

    transactions.pop(number - 1)
    save_transactions(transactions)
    print("Transaction deleted successfully!")


def save_transactions(transactions):
    with open("transactions.json", "w") as file:
        json.dump(transactions, file, indent=4)
    print("transactions saved!")


def load_transactions():
    try:
        with open("transactions.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(
            "Transaction file is corrupted or not valid JSON. Starting with an empty list.")
        return []


transactions = load_transactions()


def main():
    while True:
        print("\n===== TRANSACTION TRACKER =====")
        print("1. Add transaction")
        print("2. View transactions")
        print("3. Calculate total")
        print("4. Spending by category")
        print("5. Delete transaction")
        print("6. Save transactions")
        print("7. View Balance")
        print("8. Financial Summary")
        print("9. Edit Transaction")
        print("10. Exit")

        try:
            user_choice = int(input("Choose an option: "))

            if user_choice == 1:
                add_transaction(transactions)
            elif user_choice == 2:
                view_transaction(transactions)
            elif user_choice == 3:
                calculate_balance(transactions)
            elif user_choice == 4:
                spending_by_category(transactions)
            elif user_choice == 5:
                delete_transaction(transactions)
            elif user_choice == 6:
                save_transactions(transactions)
            elif user_choice == 7:
                display_balance(transactions)
            elif user_choice == 8:
                display_financial_summary(transactions)
            elif user_choice == 9:
                edit_transaction(transactions)
            elif user_choice == 10:
                print("Goodbye!")
                break
            else:
                print("Invalid number.")

        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()
