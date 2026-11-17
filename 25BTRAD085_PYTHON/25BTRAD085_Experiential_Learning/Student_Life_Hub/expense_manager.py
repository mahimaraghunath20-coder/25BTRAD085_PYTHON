import pandas as pd
import os

FILE_NAME = "expenses.csv"
BUDGET_FILE = "budget.csv"


# CREATE EXPENSE FILE
def create_file():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=[
            "ID", "Date", "Category", "Amount", "Description"
        ])
        df.to_csv(FILE_NAME, index=False)


# LOAD EXPENSES
def load_expenses():
    create_file()

    df = pd.read_csv(FILE_NAME)

    # Ensure correct data types
    df["ID"] = pd.to_numeric(df["ID"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    df["Date"] = df["Date"].astype("object")
    df["Category"] = df["Category"].astype("object")
    df["Description"] = df["Description"].astype("object")

    return df


# ADD EXPENSE
def add_expense(date, category, amount, description):
    df = load_expenses()

    new_id = 1 if df["ID"].dropna().empty else int(df["ID"].max()) + 1

    new_expense = pd.DataFrame([{
        "ID": new_id,
        "Date": str(date),
        "Category": str(category),
        "Amount": float(amount),
        "Description": str(description)
    }])

    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)


# UPDATE EXPENSE
def update_expense(expense_id, date, category, amount, description):
    df = load_expenses()

    mask = df["ID"] == expense_id

    df.loc[mask, "Date"] = str(date)
    df.loc[mask, "Category"] = str(category)
    df.loc[mask, "Amount"] = float(amount)
    df.loc[mask, "Description"] = str(description)

    df.to_csv(FILE_NAME, index=False)


# DELETE EXPENSE
def delete_expense(expense_id):
    df = load_expenses()

    df = df[df["ID"] != expense_id]

    df.to_csv(FILE_NAME, index=False)


# SET MONTHLY BUDGET
def set_monthly_budget(amount):
    budget_df = pd.DataFrame([{
        "Budget": float(amount)
    }])

    budget_df.to_csv(BUDGET_FILE, index=False)


# GET MONTHLY BUDGET
def get_monthly_budget():
    if not os.path.exists(BUDGET_FILE):
        set_monthly_budget(10000)
        return 10000.0

    budget_df = pd.read_csv(BUDGET_FILE)

    return float(budget_df["Budget"].iloc[0])