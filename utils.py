import json
import os
from datetime import datetime

# File paths for data storage
EXPENSE_FILE = "expenses.json"
BUDGET_FILE = "budgets.json"
INVESTMENT_FILE = "investments.json"
USER_FILE = "users.json"

# Category colors for consistent visualization
CATEGORY_COLORS = {
    "Food & Dining": "#4b64e6",
    "Rent": "#48c28a",
    "Transportation": "#4ca3e6",
    "Shopping": "#e6c84a",
    "Education": "#a64ae6",
    "Entertainment": "#e64a6c",
    "Others": "#e64a4a"
}

# Helper functions for data management
def get_expense_data():
    """Load expense data from file or return empty list if file doesn't exist"""
    if os.path.exists(EXPENSE_FILE):
        try:
            with open(EXPENSE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_expense_data(data):
    """Save expense data to file"""
    with open(EXPENSE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_budget_data():
    """Load budget data from file or return empty list if file doesn't exist"""
    if os.path.exists(BUDGET_FILE):
        try:
            with open(BUDGET_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_budget_data(data):
    """Save budget data to file"""
    with open(BUDGET_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_investment_data():
    """Load investment data from file or return empty list if file doesn't exist"""
    if os.path.exists(INVESTMENT_FILE):
        try:
            with open(INVESTMENT_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_investment_data(data):
    """Save investment data to file"""
    with open(INVESTMENT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user_data():
    """Load user data from file or return empty dict if file doesn't exist"""
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_user_data(data):
    """Save user data to file"""
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_color_for_category(category):
    """Get color for a category, with fallback for unknown categories"""
    return CATEGORY_COLORS.get(category, "#808080")

def calculate_monthly_summary(expenses, month):
    """Calculate total expenses and category breakdown for a specific month"""
    month_expenses = [exp for exp in expenses if exp.get('date', '').startswith(month)]
    
    total = sum(exp.get('amount', 0) for exp in month_expenses)
    
    categories = {}
    for expense in month_expenses:
        category = expense.get('category', 'Others')
        amount = expense.get('amount', 0)
        categories[category] = categories.get(category, 0) + amount
    
    return {
        'total': total,
        'categories': categories
    }

def format_currency(amount):
    """Format amount as Indian currency (₹)"""
    return f"₹{amount:,.2f}"

def calculate_date_range(period):
    """Calculate start and end dates based on period"""
    today = datetime.now()
    
    if period == "This Month":
        start_date = today.replace(day=1)
        end_date = today
    elif period == "Last Month":
        last_month = today.replace(day=1)
        last_month = last_month.replace(day=1) - timedelta(days=1)
        start_date = last_month.replace(day=1)
        end_date = last_month
    elif period == "Last 3 Months":
        start_date = today - timedelta(days=90)
        end_date = today
    elif period == "Last 6 Months":
        start_date = today - timedelta(days=180)
        end_date = today
    elif period == "This Year":
        start_date = today.replace(month=1, day=1)
        end_date = today
    else:  # All Time
        start_date = None
        end_date = None
    
    return start_date, end_date
