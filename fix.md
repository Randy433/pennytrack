Randy, excellent choice! This is an important step in moving from writing beginner Python programs to designing software that is easier to test, maintain, and extend.

We're going to learn how to **separate calculation from display** using your existing `spending_by_category()` function.

I'll explain the idea first, then we'll build it step by step.

# 1. Understand the problem with your current function

Your current function performs two jobs:

1. Calculates how much was spent in each category.
2. Displays the results to the user.

For example:

```python
def spending_by_category(transactions):
    category_total = {}

    for transaction in transactions:
        category = transaction["category"]

        if category in category_total:
            category_total[category] += transaction["amount"]
        else:
            category_total[category] = transaction["amount"]

    print("\n===== SPENDING BY CATEGORY =====")

    if not category_total:
        print("No transactions found.")
        return

    for category, total in category_total.items():
        print(f"{category}: ₦{total:,.2f}")
```

This function works. The problem isn't that your code is incorrect.

**The problem is that calculation and display are mixed together.**

Imagine you later want to:
- Display the report in your terminal.
- Show the same report on a website.
- Export the report to a CSV file.
- Test the calculation automatically.

If the calculation is tied to printing, you'll have less flexibility.

Let's fix that.

---

# 2. Understand the difference between `print()` and `return`

Before separating the functions, you need to understand one important distinction.

### `print()` displays information

```python
def calculate_total():
    total = 5000
    print(total)
```

Calling the function:

```python
calculate_total()
```

Displays:

```text
5000
```

But the function doesn't explicitly return the calculated value.

### `return` gives a value back to the caller

```python
def calculate_total():
    total = 5000
    return total
```

Now consider:

```python
result = calculate_total()

print(result)
```

Output:

```text
5000
```

What's different?

When Python executes `return total`, the function sends the value back to the code that called it.

That code can then:
- Print the value.
- Save it to a variable.
- Compare it with another value.
- Use it in another calculation.
- Test whether it's correct.

**Think of `return` as making the result available to the rest of your program, while `print()` displays information to the user.**

A function can use both, but separating their responsibilities often makes your code easier to work with.

---

# 3. Step one: Create a function that calculates category totals

Let's take the calculation part of your existing function and move it into a separate function.

```python
def calculate_spending_by_category(transactions):
    category_total = {}

    for transaction in transactions:
        category = transaction["category"]

        if category in category_total:
            category_total[category] += transaction["amount"]
        else:
            category_total[category] = transaction["amount"]

    return category_total
```

Let's understand what this function does.

### First: Create an empty dictionary

```python
category_total = {}
```

This dictionary will store each category and its accumulated spending.

### Second: Go through every transaction

```python
for transaction in transactions:
```

Each transaction is a dictionary containing information such as its amount and category.

For example:

```python
{
    "amount": 5000,
    "category": "Food",
    "description": "Groceries"
}
```

### Third: Get the category

```python
category = transaction["category"]
```

For the example above, `category` becomes `"Food"`.

### Fourth: Calculate the totals

```python
if category in category_total:
    category_total[category] += transaction["amount"]
else:
    category_total[category] = transaction["amount"]
```

If the category already exists, add the new amount to its existing total.

Otherwise, create a new entry for that category.

### Fifth: Return the result

```python
return category_total
```

This is the key change.

Instead of printing the dictionary, the function returns it.

Suppose you have these transactions:

```python
transactions = [
    {"amount": 5000, "category": "Food", "description": "Groceries"},
    {"amount": 2000, "category": "Transport", "description": "Bus fare"},
    {"amount": 3000, "category": "Food", "description": "Lunch"}
]
```

You can call the function:

```python
result = calculate_spending_by_category(transactions)
```

The variable `result` now refers to this dictionary:

```python
{
    "Food": 8000,
    "Transport": 2000
}
```

Nothing has been printed yet. The calculation function simply produces and returns the result.

---

# 4. Step two: Create a separate function to display the results

Now that the calculation function returns a dictionary, we can create another function whose only job is to display that dictionary.

```python
def display_spending_by_category(category_total):
    print("\n===== SPENDING BY CATEGORY =====")

    if not category_total:
        print("No transactions found.")
        return

    for category, total in category_total.items():
        print(f"{category}: ₦{total:,.2f}")
```

Notice the parameter:

```python
def display_spending_by_category(category_total):
```

This function receives the dictionary that the calculation function returns.

It doesn't need to know how the totals were calculated. It only needs the finished results.

The loop:

```python
for category, total in category_total.items():
```

retrieves each category and its corresponding total.

The f-string formats each result for display.

For example:

```text
===== SPENDING BY CATEGORY =====
Food: ₦8,000.00
Transport: ₦2,000.00
```

The display function doesn't perform any spending calculations.

**Its only responsibility is to present the data.**

---

# 5. Step three: Connect the two functions

Now we need to use the two functions together.

You can replace your old `spending_by_category()` function with this version:

```python
def spending_by_category(transactions):
    category_total = calculate_spending_by_category(transactions)

    display_spending_by_category(category_total)
```

Let's trace the execution.

Suppose your main program calls:

```python
spending_by_category(transactions)
```

Python follows these steps:

**Step 1:** It calls `calculate_spending_by_category(transactions)`.

**Step 2:** That function calculates the totals and returns a dictionary.

**Step 3:** The returned dictionary is assigned to `category_total`.

**Step 4:** Python passes that dictionary to `display_spending_by_category()`.

**Step 5:** The display function prints the report.

The complete flow looks like this:

```text
transactions
     |
     v
calculate_spending_by_category()
     |
     v
Returns a dictionary
     |
     v
display_spending_by_category()
     |
     v
Formatted report
```

This is called **separation of responsibilities**: each function has a clear job.

---

# 6. Why does this make automated testing easier?

This is where the real benefit becomes clear.

Suppose you want to verify that Food spending totals ₦8,000.

With the calculation separated, you can test the returned dictionary directly:

```python
transactions = [
    {"amount": 5000, "category": "Food", "description": "Groceries"},
    {"amount": 2000, "category": "Transport", "description": "Bus fare"},
    {"amount": 3000, "category": "Food", "description": "Lunch"}
]

result = calculate_spending_by_category(transactions)

print(result["Food"])
```

Output:

```text
8000
```

You don't have to inspect the formatted report or capture anything printed to the terminal.

Later, with `unittest`, you can write:

```python
self.assertEqual(result["Food"], 8000)
```

Python can check whether the result matches the expected value automatically.

You can also test whether Transport totals ₦2,000.

This is easier because your calculation function returns data instead of only displaying it.

### Another benefit: Reusability

Imagine you build a web application later.

Your website can use `calculate_spending_by_category()` to obtain the totals, then display them in a table or chart.

You won't need to rewrite the calculation logic just because the presentation has changed.

That's one reason this pattern is useful in real-world software engineering.

---

# 7. Your assignment

Now I want you to apply this pattern to your existing PennyTrack project.

Create these three functions:

| Function | Responsibility |
|---|---|
| `calculate_spending_by_category(transactions)` | Calculate and return the category totals. |
| `display_spending_by_category(category_total)` | Display the returned dictionary in a readable format. |
| `spending_by_category(transactions)` | Connect the calculation and display functions. |

Use the examples above as your guide.

### Test your implementation

Use these transactions:

```python
transactions = [
    {"amount": 5000, "category": "Food", "description": "Groceries"},
    {"amount": 2000, "category": "Transport", "description": "Bus fare"},
    {"amount": 3000, "category": "Food", "description": "Lunch"}
]
```

Your report should show:

```text
===== SPENDING BY CATEGORY =====
Food: ₦8,000.00
Transport: ₦2,000.00
```

Also test an empty transaction list.

It should display:

```text
===== SPENDING BY CATEGORY =====
No transactions found.
```

## One final question to check your understanding

Suppose you write:

```python
def calculate_total(transactions):
    total = 5000
    return total
```

Then you call:

```python
result = calculate_total(transactions)
```

**What does the variable `result` contain after the function finishes?**

A. Nothing, because the function doesn't use `print()`.

B. The number `5000`, returned by the function.

C. The text `"5000"`.

D. The entire `transactions` list.

Choose your answer, and then send me your three updated functions. I'll review your implementation before we move on to automated testing.