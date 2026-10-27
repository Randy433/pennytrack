# PennyTrack 💰

PennyTrack is a personal finance tracker built with Python and Flask. It helps users record income and expenses, monitor their balance, and understand their spending by category through a simple web interface.

## Features

 **Add Transactions:** Record income and expenses with an amount, category, and description.
 **View Transactions:** Display recorded transactions on the dashboard.
 **Edit Transactions:** Update existing transaction details.
 **Delete Transactions:** Remove transactions you no longer need.
 **Balance Calculation:** Calculate the remaining balance by subtracting total expenses from total income.
 **Spending by Category:** Organize expenses by category to understand spending patterns.
 **Financial Summary:** View a summary of income, expenses, and remaining balance.
 **Input Validation:** Validate transaction details to help prevent invalid records.
 **Data Persistence:** Store transactions in a JSON file so they remain available after restarting the application.
 **Automated Tests:** Test core functionality, transaction validation, and web routes.

## Technologies Used

 Python
 Flask
 HTML
 CSS
 JSON
 `unittest`

## Project Structure

PennyTrack/
├── app.py
├── pennytrack.py
├── test_pennytrack.py
├── requirements.txt
├── transactions.json
├── templates/
│   ├── index.html
│   └── edit_transaction.html
└── static/
    └── css/
        └── style.css

## Getting Started

### Prerequisites

Before running PennyTrack, ensure you have:

 Python 3 installed.
 `pip` available for installing Python packages.

### 1. Clone the Repository

If you have uploaded PennyTrack to GitHub, clone it using:

```bash
git clone <your-repository-url>
```

Navigate into the project directory:

```bash
cd PennyTrack
```

Replace `<your-repository-url>` with your actual GitHub repository URL.

### 2. Create a Virtual Environment

A virtual environment keeps your project's Python dependencies separate from other projects.

```bash
python3 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows, use:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

Start the Flask development server:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

You should now be able to interact with PennyTrack through its web interface.

## Running the Tests

PennyTrack uses Python's builtin `unittest` framework.

Run the test suite from the project directory:

```bash
python -m unittest -v
```

The tests cover transaction calculations, input validation, data persistence, and web application routes.

## Data Storage

PennyTrack stores transaction records in `transactions.json`.

Each transaction contains:

 `amount`: The transaction amount.
 `type`: The transaction type (`income` or `expense`).
 `category`: The transaction category.
 `description`: A description of the transaction.

**Note:** Keep a backup of `transactions.json` if it contains financial records you want to preserve.

## Current Status

PennyTrack is an ongoing learning project focused on applying Python programming, automated testing, and Flask web development to a practical application.

## Future Improvements

Potential future enhancements include:

 User registration and authentication.
 A database for more robust data storage.
 Monthly and yearly financial reports.
 Spending charts and visualizations.
 Improved mobile responsiveness.
 Deployment

## Author
# Ridwan AbdulGaniyu

Developed as a personal project to strengthen Python and web development skills.