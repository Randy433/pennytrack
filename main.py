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
        else:
            break
    category = input("Enter the category: ")
    description = input("Enter the description: ")

    transaction = {
        "amount": amount,
        "category": category,
        "description": description
    }

    transactions.append(transaction)
    save_transactions(transactions)
    print("transactions Added")


def view_transaction(transactions):
    if not transactions:
        print("No transaction found")
        return
    for number, transaction in enumerate(transactions, start=1):
        print(
            f"{number}. {transaction['amount']}\t{transaction['category']}\t{transaction['description']}")


def calculate_balance(transactions):
    total = 0
    for transaction in transactions:
        total += transaction["amount"]
    print("===== TOTAL EXPENSES =====")
    print(f"Total spent: ₦{total:,.2f}")


def spending_by_category(transactions):
    category_total = {}
    for transaction in transactions:
        if transaction["category"] in category_total:
            category_total[transaction["category"]
                           ] = category_total[transaction["category"]] + transaction["amount"]
        else:
            category_total[transaction["category"]] = transaction["amount"]
    print("\n===== SPENDING BY CATEGORY =====")
    if not category_total:
        print("No transactions found.")
        return
    for category, total in category_total.items():
        print(f"{category}: ₦{total:,.2f}")


def delete_transaction(transactions):
    if len(transactions) == 0:
        print("The transaction is empty")
        return
    view_transaction(transactions)
    number = int(input("Which transaction do you want to delete? ")) - 1
    if number >= 0 and number < len(transactions):
        transactions.pop(number)
        print("transactions deleted!")
    else:
        print("Invalid transactions number.")
    save_transactions(transactions)


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

while True:

    print("\n===== Transaction TRACKER =====")
    print("1. Add transaction")
    print("2. View transactions")
    print("3. Calculate total")
    print("4. Spending by category")
    print("5. Delete transaction")
    print("6. Save transactions")
    print("7. Exit")

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
            print("Goodbye")
            break
        else:
            print("Invalid number")
    except ValueError:
        print("Please enter a valid number")
