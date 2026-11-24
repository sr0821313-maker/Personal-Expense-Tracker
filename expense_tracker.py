import os
from datetime import datetime

import pandas as pd

FILE_NAME = "expenses.csv"
COLUMNS = ["Date", "Category", "Description", "Amount"]


def initialize_file():
    """Create the CSV file with the required columns if it does not exist."""
    if not os.path.exists(FILE_NAME):
        pd.DataFrame(columns=COLUMNS).to_csv(FILE_NAME, index=False)


def read_expenses():
    """Read saved expenses from the CSV file."""
    initialize_file()
    try:
        df = pd.read_csv(FILE_NAME)
        if list(df.columns) != COLUMNS:
            print("Error: expenses.csv must contain Date, Category, Description, Amount columns.")
            return None
        return df
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as error:
        print(f"Could not read expenses.csv: {error}")
        return None


def add_expense():
    """Get details, validate them, and append one expense to the CSV file."""
    print("\n--- Add Expense ---")
    date_text = input("Enter date (YYYY-MM-DD): ").strip()

    try:
        # Also checks that the date is a real calendar date.
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD. Expense not saved.")
        return

    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()
    amount_text = input("Enter amount: ").strip()

    if not category:
        print("Invalid category. Category cannot be empty. Expense not saved.")
        return
    if not description:
        print("Invalid description. Description cannot be empty. Expense not saved.")
        return

    try:
        amount = float(amount_text)
        if amount <= 0:
            print("Invalid amount. Amount must be a positive number. Expense not saved.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number. Expense not saved.")
        return

    df = read_expenses()
    if df is None:
        return

    new_row = pd.DataFrame(
        [[date_text, category, description, amount]],
        columns=COLUMNS
    )
    updated = pd.concat([df, new_row], ignore_index=True)

    try:
        updated.to_csv(FILE_NAME, index=False)
        print(f"Expense saved. Total records: {len(updated)}")
    except OSError as error:
        print(f"Could not save expense: {error}")


def show_expenses():
    """Display all saved expense records."""
    print("\n--- All Expenses ---")
    df = read_expenses()
    if df is None:
        return
    if df.empty:
        print("No expenses recorded yet.")
        return

    print(df.to_string(index=False))


def category_summary():
    """Display total spending for each category and the grand total."""
    print("\n--- Category Summary ---")
    df = read_expenses()
    if df is None:
        return
    if df.empty:
        print("No expenses recorded yet.")
        return

    # Pandas groupby() combines rows with the same category and sums Amount.
    summary = df.groupby("Category")["Amount"].sum()

    for category, total in summary.items():
        print(f"{category}: {total:g}")

    print(f"Total: {df['Amount'].sum():g}")


def monthly_summary():
    """Display total spending for each month (YYYY-MM)."""
    print("\n--- Monthly Summary ---")
    df = read_expenses()
    if df is None:
        return
    if df.empty:
        print("No expenses recorded yet.")
        return

    df["Month"] = pd.to_datetime(df["Date"], format="%Y-%m-%d").dt.strftime("%Y-%m")
    summary = df.groupby("Month")["Amount"].sum()

    for month, total in summary.items():
        print(f"{month}: {total:g}")

    print(f"Total: {df['Amount'].sum():g}")


def main():
    initialize_file()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. Show All Expenses")
        print("3. Category Summary")
        print("4. Monthly Summary")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            category_summary()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            print("Thank you for using Personal Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
