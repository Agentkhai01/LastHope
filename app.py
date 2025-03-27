import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import os
from utils import (
    get_expense_data, save_expense_data, get_budget_data, save_budget_data,
    get_investment_data, save_investment_data, get_user_data, save_user_data,
    get_color_for_category, calculate_monthly_summary
)
from investment_calculator import calculate_sip_returns, calculate_lumpsum_returns
from humor_tips import get_random_tip
from gamification import get_achievement, update_points

# Page configuration
st.set_page_config(
    page_title="FinSmart - Self Finance Management Platform",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'login_status' not in st.session_state:
    st.session_state.login_status = False
    st.session_state.username = ""
    st.session_state.current_page = "dashboard"
    st.session_state.points = 0
    st.session_state.achievements = []
    st.session_state.tip_shown = False
    st.session_state.last_tip = ""

# Header with logo
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.markdown("""
    <div style="display: flex; align-items: center;">
        <svg width="30" height="30" viewBox="0 0 24 24" style="margin-right: 10px;">
            <path fill="white" d="M21,18V19A2,2 0 0,1 19,21H5A2,2 0 0,1 3,19V5A2,2 0 0,1 5,3H19A2,2 0 0,1 21,5V6H12C10.89,6 10,6.9 10,8V16A2,2 0 0,0 12,18H21M12,16H22V8H12V16M16,13.5A1.5,1.5 0 0,1 14.5,12A1.5,1.5 0 0,1 16,10.5A1.5,1.5 0 0,1 17.5,12A1.5,1.5 0 0,1 16,13.5Z" />
        </svg>
        <span style="font-size: 24px; font-weight: bold;">FinSmart</span>
    </div>
    """, unsafe_allow_html=True)

# Login Page
def show_login_page():
    st.title("Welcome to FinSmart")
    st.subheader("Your Personal Finance Manager")
    
    tip = get_random_tip()
    st.info(f"💡 **Financial Tip:** {tip}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Simple login for demo purposes
            if username and password:
                st.session_state.login_status = True
                st.session_state.username = username
                st.session_state.points = 100  # Initial points
                st.rerun()
            else:
                st.error("Please enter username and password")
    
    with col2:
        st.subheader("Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords don't match")
            elif new_username and new_password:
                # Simple registration for demo purposes
                user_data = get_user_data()
                user_data[new_username] = {
                    "password": new_password,
                    "points": 100,
                    "achievements": [],
                    "joined_date": datetime.now().strftime("%Y-%m-%d")
                }
                save_user_data(user_data)
                st.success("Registration successful! You can now login.")
            else:
                st.error("Please fill all fields")

# Main App
def show_main_app():
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### Hello, {st.session_state.username}!")
        st.markdown(f"**Points:** 🌟 {st.session_state.points}")
        
        # Show a random achievement if achieved
        if not st.session_state.tip_shown and random.random() < 0.3:  # 30% chance to show a tip
            tip = get_random_tip()
            st.session_state.last_tip = tip
            st.session_state.tip_shown = True
            st.info(f"💡 **Tip of the day:** {tip}")
        
        # Navigation
        st.subheader("Navigation")
        if st.button("Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
        if st.button("Expenses", use_container_width=True):
            st.session_state.current_page = "expenses"
            st.rerun()
        if st.button("Budget", use_container_width=True):
            st.session_state.current_page = "budget"
            st.rerun()
        if st.button("Investments", use_container_width=True):
            st.session_state.current_page = "investments"
            st.rerun()
        if st.button("Financial Assistant", use_container_width=True):
            st.session_state.current_page = "financial_assistant"
            st.rerun()
        
        st.markdown("---")
        
        # Gamification section
        st.subheader("Achievements")
        achievement = get_achievement(st.session_state.points)
        if achievement:
            st.success(f"🏆 {achievement}")
        
        if st.button("Logout"):
            st.session_state.login_status = False
            st.session_state.username = ""
            st.rerun()
    
    # Main content based on current page
    if st.session_state.current_page == "dashboard":
        show_dashboard()
    elif st.session_state.current_page == "expenses":
        show_expenses()
    elif st.session_state.current_page == "budget":
        show_budget()
    elif st.session_state.current_page == "investments":
        show_investments()
    elif st.session_state.current_page == "financial_assistant":
        show_financial_assistant()

def show_dashboard():
    st.title("Dashboard")
    
    # Get user data
    expense_data = get_expense_data()
    budget_data = get_budget_data()
    investment_data = get_investment_data()
    
    # Filter for current user
    user_expenses = [exp for exp in expense_data if exp.get('username') == st.session_state.username]
    user_budget = next((b for b in budget_data if b.get('username') == st.session_state.username), 
                       {"monthly_budget": 10000, "savings_target": 3000})
    user_investments = [inv for inv in investment_data if inv.get('username') == st.session_state.username]
    
    # Calculate monthly summary
    current_month = datetime.now().strftime("%Y-%m")
    monthly_summary = calculate_monthly_summary(user_expenses, current_month)
    
    # Top stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        monthly_spent = monthly_summary.get('total', 0)
        monthly_budget = user_budget.get('monthly_budget', 10000)
        percentage = round((monthly_spent / monthly_budget) * 100, 1) if monthly_budget else 0
        change = "-8.5%" if percentage < 100 else f"+{percentage - 100:.1f}%"
        
        st.markdown(f"""
        <div style='background-color: #1E2A4A; padding: 20px; border-radius: 10px;'>
            <p style='color: gray;'>Monthly Spent</p>
            <h2 style='margin:0;'>₹{monthly_spent:,}</h2>
            <p style='margin:0;'>out of ₹{monthly_budget:,}</p>
            <p style='color: {"red" if percentage >= 100 else "green"};'>{change}</p>
            <div style='background-color: #444; height: 10px; border-radius: 5px; margin-top: 10px;'>
                <div style='background-color: {"red" if percentage >= 100 else "#FF5733"}; width: {min(percentage, 100)}%; 
                height: 100%; border-radius: 5px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        monthly_saved = user_budget.get('savings_target', 3000) - monthly_summary.get('total', 0)
        monthly_saved = max(0, monthly_saved)
        savings_target = user_budget.get('savings_target', 3000)
        percentage = round((monthly_saved / savings_target) * 100, 1) if savings_target else 0
        
        st.markdown(f"""
        <div style='background-color: #1E2A4A; padding: 20px; border-radius: 10px;'>
            <p style='color: gray;'>Monthly Savings</p>
            <h2 style='margin:0;'>₹{monthly_saved:,}</h2>
            <p style='margin:0;'>target ₹{savings_target:,}</p>
            <p style='color: {"green" if monthly_saved > 0 else "red"};'>+12.3%</p>
            <div style='background-color: #444; height: 10px; border-radius: 5px; margin-top: 10px;'>
                <div style='background-color: #4CAF50; width: {min(percentage, 100)}%; 
                height: 100%; border-radius: 5px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_invested = sum(inv.get('amount', 0) for inv in user_investments)
        investment_growth = sum(inv.get('growth', 0) for inv in user_investments)
        
        st.markdown(f"""
        <div style='background-color: #1E2A4A; padding: 20px; border-radius: 10px;'>
            <p style='color: gray;'>Investments</p>
            <h2 style='margin:0;'>₹{total_invested:,}</h2>
            <p style='margin:0;'>total growth ₹{investment_growth:,}</p>
            <p style='color: green;'>+5.7%</p>
            <div style='background-color: #444; height: 10px; border-radius: 5px; margin-top: 10px;'>
                <div style='background-color: #3F51B5; width: 75%; height: 100%; border-radius: 5px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Expense breakdown and Add Expense
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Expense Breakdown")
        
        # Create expense category summary
        categories = {}
        for expense in user_expenses:
            if expense.get('date', '').startswith(current_month):
                category = expense.get('category', 'Others')
                amount = expense.get('amount', 0)
                categories[category] = categories.get(category, 0) + amount
        
        if categories:
            # Calculate percentages
            total = sum(categories.values())
            categories_with_pct = {k: (v, round(v / total * 100)) for k, v in categories.items()}
            
            # Sort by amount (descending)
            sorted_categories = sorted(categories_with_pct.items(), key=lambda x: x[1][0], reverse=True)
            
            # Create a pie chart
            labels = [cat for cat, _ in sorted_categories]
            values = [val[0] for _, val in sorted_categories]
            colors = [get_color_for_category(cat) for cat in labels]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.4,
                marker_colors=colors
            )])
            
            fig.update_layout(
                margin=dict(t=0, b=0, l=0, r=0),
                height=300,
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show category breakdown as text
            st.markdown("### Category Breakdown")
            for category, (amount, percentage) in sorted_categories:
                color = get_color_for_category(category)
                st.markdown(f"""
                <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                    <div>
                        <span style='color: {color}; font-size: 12px;'>●</span> {category}
                    </div>
                    <div>
                        ₹{amount:,} ({percentage}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No expenses recorded for this month. Add your first expense to see the breakdown.")
    
    with col2:
        st.subheader("Add Expense")
        with st.form("add_expense_form"):
            amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0, format="%.2f")
            
            category = st.selectbox(
                "Category",
                ["Food & Dining", "Rent", "Transportation", "Shopping", "Education", "Entertainment", "Others"]
            )
            
            date = st.date_input("Date", datetime.now())
            
            description = st.text_input("Description", placeholder="e.g. Lunch with friends")
            
            submitted = st.form_submit_button("Add Expense", use_container_width=True)
            
            if submitted:
                if amount > 0:
                    # Add the expense
                    new_expense = {
                        "username": st.session_state.username,
                        "amount": amount,
                        "category": category,
                        "date": date.strftime("%Y-%m-%d"),
                        "description": description,
                        "id": str(random.randint(10000, 99999))
                    }
                    
                    expense_data.append(new_expense)
                    save_expense_data(expense_data)
                    
                    # Update points
                    st.session_state.points += 5
                    st.success("Expense added successfully! You earned 5 points.")
                    
                    # Check for milestone achievement
                    achievement = update_points(st.session_state.points)
                    if achievement:
                        st.balloons()
                        st.success(f"🏆 Achievement unlocked: {achievement}")
                    
                    st.rerun()
                else:
                    st.error("Amount must be greater than 0")

def show_expenses():
    st.title("Expense Tracker")
    
    # Get expense data
    expense_data = get_expense_data()
    user_expenses = [exp for exp in expense_data if exp.get('username') == st.session_state.username]
    
    # Date filter
    col1, col2 = st.columns(2)
    with col1:
        filter_option = st.selectbox(
            "Filter by",
            ["All Time", "This Month", "Last Month", "Last 3 Months", "Custom Date Range"]
        )
    
    start_date = None
    end_date = None
    
    if filter_option == "This Month":
        start_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
    elif filter_option == "Last Month":
        last_month = datetime.now().replace(day=1) - timedelta(days=1)
        start_date = last_month.replace(day=1).strftime("%Y-%m-%d")
        end_date = last_month.strftime("%Y-%m-%d")
    elif filter_option == "Last 3 Months":
        three_months_ago = datetime.now() - timedelta(days=90)
        start_date = three_months_ago.strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
    elif filter_option == "Custom Date Range":
        with col2:
            date_range = st.date_input(
                "Select date range",
                value=(datetime.now() - timedelta(days=30), datetime.now()),
                max_value=datetime.now()
            )
            if len(date_range) == 2:
                start_date = date_range[0].strftime("%Y-%m-%d")
                end_date = date_range[1].strftime("%Y-%m-%d")
    
    # Filter expenses by date
    filtered_expenses = user_expenses
    if start_date and end_date:
        filtered_expenses = [
            exp for exp in user_expenses 
            if start_date <= exp.get('date', '') <= end_date
        ]
    
    # Add new expense
    with st.expander("Add New Expense"):
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0, format="%.2f")
            category = st.selectbox(
                "Category",
                ["Food & Dining", "Rent", "Transportation", "Shopping", "Education", "Entertainment", "Others"]
            )
        
        with col2:
            date = st.date_input("Date", datetime.now())
            description = st.text_input("Description", placeholder="e.g. Lunch with friends")
        
        if st.button("Add Expense", use_container_width=True):
            if amount > 0:
                # Add the expense
                new_expense = {
                    "username": st.session_state.username,
                    "amount": amount,
                    "category": category,
                    "date": date.strftime("%Y-%m-%d"),
                    "description": description,
                    "id": str(random.randint(10000, 99999))
                }
                
                expense_data.append(new_expense)
                save_expense_data(expense_data)
                
                # Update points
                st.session_state.points += 5
                st.success("Expense added successfully! You earned 5 points.")
                st.rerun()
            else:
                st.error("Amount must be greater than 0")
    
    # Display expense summary
    if filtered_expenses:
        # Calculate totals by category
        categories = {}
        for expense in filtered_expenses:
            category = expense.get('category', 'Others')
            amount = expense.get('amount', 0)
            categories[category] = categories.get(category, 0) + amount
        
        total_expense = sum(categories.values())
        
        # Show summary
        st.subheader("Expense Summary")
        st.markdown(f"**Total Expenses:** ₹{total_expense:,.2f}")
        
        # Create a bar chart for category breakdown
        category_df = pd.DataFrame({
            'Category': list(categories.keys()),
            'Amount': list(categories.values())
        })
        
        fig = px.bar(
            category_df, 
            x='Category', 
            y='Amount',
            color='Category',
            color_discrete_map={cat: get_color_for_category(cat) for cat in categories.keys()},
            title="Expenses by Category"
        )
        
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Amount (₹)",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Daily expense trend
        st.subheader("Daily Expense Trend")
        
        # Group expenses by date
        date_expenses = {}
        for expense in filtered_expenses:
            date = expense.get('date', '')
            amount = expense.get('amount', 0)
            date_expenses[date] = date_expenses.get(date, 0) + amount
        
        # Create a line chart for daily expenses
        date_df = pd.DataFrame({
            'Date': list(date_expenses.keys()),
            'Amount': list(date_expenses.values())
        })
        
        date_df['Date'] = pd.to_datetime(date_df['Date'])
        date_df = date_df.sort_values('Date')
        
        fig = px.line(
            date_df,
            x='Date',
            y='Amount',
            markers=True,
            title="Daily Expense Trend"
        )
        
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Amount (₹)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # List all expenses
        st.subheader("Expense List")
        
        # Sort expenses by date (newest first)
        sorted_expenses = sorted(filtered_expenses, key=lambda x: x.get('date', ''), reverse=True)
        
        for expense in sorted_expenses:
            col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
            
            with col1:
                st.markdown(f"**₹{expense.get('amount', 0):,.2f}**")
            
            with col2:
                desc = expense.get('description', '')
                cat = expense.get('category', 'Others')
                color = get_color_for_category(cat)
                st.markdown(f"{desc} <span style='color: {color}; background-color: rgba(0,0,0,0.1); padding: 2px 6px; border-radius: 10px; font-size: 0.8em;'>{cat}</span>", unsafe_allow_html=True)
            
            with col3:
                date_str = expense.get('date', '')
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%d %b %Y")
                    st.markdown(f"{formatted_date}")
                except:
                    st.markdown(f"{date_str}")
            
            with col4:
                expense_id = expense.get('id', '')
                if st.button("🗑️", key=f"delete_{expense_id}"):
                    # Remove the expense
                    expense_data = [exp for exp in expense_data if exp.get('id') != expense_id]
                    save_expense_data(expense_data)
                    st.success("Expense deleted successfully!")
                    st.rerun()
            
            st.markdown("---")
    else:
        st.info("No expenses found for the selected period. Add your first expense to see the summary.")
        
        # Humorous tip for motivation
        st.markdown("""
        > 😎 **Pro Tip:** Tracking every expense is like detective work, but instead of finding criminals, 
        > you find where your money disappears to! Start with your first case now.
        """)

def show_budget():
    st.title("Budget Planner")
    
    # Get budget data
    budget_data = get_budget_data()
    user_budget = next((b for b in budget_data if b.get('username') == st.session_state.username), None)
    
    # Get expense data for comparison
    expense_data = get_expense_data()
    user_expenses = [exp for exp in expense_data if exp.get('username') == st.session_state.username]
    
    # Current month and year
    current_month = datetime.now().strftime("%Y-%m")
    month_name = datetime.now().strftime("%B %Y")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Budget for {month_name}")
        
        if user_budget:
            monthly_budget = user_budget.get('monthly_budget', 10000)
            savings_target = user_budget.get('savings_target', 3000)
            
            # Budget categories
            categories = user_budget.get('categories', {
                "Food & Dining": 0.3,
                "Rent": 0.4,
                "Transportation": 0.1,
                "Shopping": 0.1,
                "Others": 0.1
            })
            
            # Calculate monthly expenses
            monthly_expenses = sum(exp.get('amount', 0) for exp in user_expenses 
                                  if exp.get('date', '').startswith(current_month))
            
            # Calculate remaining budget
            remaining_budget = monthly_budget - monthly_expenses
            
            # Progress bar for overall budget
            percentage_used = min(100, round((monthly_expenses / monthly_budget) * 100, 1)) if monthly_budget else 0
            
            st.markdown(f"### Monthly Budget: ₹{monthly_budget:,}")
            st.progress(percentage_used / 100)
            st.markdown(f"**Used:** ₹{monthly_expenses:,} ({percentage_used}%) - **Remaining:** ₹{remaining_budget:,} ({100-percentage_used}%)")
            
            # Budget by category
            st.markdown("### Budget Allocation")
            
            # Calculate expenses by category
            category_expenses = {}
            for expense in user_expenses:
                if expense.get('date', '').startswith(current_month):
                    category = expense.get('category', 'Others')
                    amount = expense.get('amount', 0)
                    category_expenses[category] = category_expenses.get(category, 0) + amount
            
            # Create a dataframe for the budget vs. actual
            budget_df = []
            
            for category, percentage in categories.items():
                allocated_amount = monthly_budget * percentage
                spent_amount = category_expenses.get(category, 0)
                remaining_amount = allocated_amount - spent_amount
                percentage_used = min(100, round((spent_amount / allocated_amount) * 100, 1)) if allocated_amount else 0
                
                budget_df.append({
                    'Category': category,
                    'Allocated': allocated_amount,
                    'Spent': spent_amount,
                    'Remaining': remaining_amount,
                    'Percentage': percentage_used
                })
            
            # Add categories that have expenses but no allocation
            for category in category_expenses:
                if category not in categories:
                    spent_amount = category_expenses[category]
                    budget_df.append({
                        'Category': category,
                        'Allocated': 0,
                        'Spent': spent_amount,
                        'Remaining': -spent_amount,
                        'Percentage': 100
                    })
            
            # Display budget vs. actual
            for item in budget_df:
                cat = item['Category']
                allocated = item['Allocated']
                spent = item['Spent']
                remaining = item['Remaining']
                percentage = item['Percentage']
                
                color = get_color_for_category(cat)
                
                st.markdown(f"""
                <div style='margin-bottom: 15px;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: {color};'>● {cat}</span>
                        <span>₹{spent:,} / ₹{allocated:,}</span>
                    </div>
                    <div style='background-color: #444; height: 8px; border-radius: 4px; margin-top: 5px;'>
                        <div style='background-color: {color}; width: {percentage}%; 
                        height: 100%; border-radius: 4px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Savings progress
            st.markdown("### Savings Target")
            estimated_savings = monthly_budget - monthly_expenses
            savings_percentage = min(100, round((estimated_savings / savings_target) * 100, 1)) if savings_target else 0
            
            st.progress(savings_percentage / 100)
            st.markdown(f"**Target:** ₹{savings_target:,} - **Current:** ₹{max(0, estimated_savings):,} ({savings_percentage}%)")
            
            # Humorous tip
            if percentage_used > 80:
                st.warning("⚠️ **Budget Alert:** Your spending is approaching your budget limit. Time to activate stealth mode for your wallet!")
            elif savings_percentage > 80:
                st.success("🎉 **Savings Hero:** You're crushing your savings goal! Your future self is already thanking you.")
        
        else:
            st.info("You haven't set up your budget yet. Use the form on the right to create your first budget.")
    
    with col2:
        st.subheader("Set Your Budget")
        
        with st.form("budget_form"):
            monthly_budget = st.number_input(
                "Monthly Budget (₹)",
                min_value=1000,
                step=1000,
                value=user_budget.get('monthly_budget', 10000) if user_budget else 10000
            )
            
            savings_target = st.number_input(
                "Savings Target (₹)",
                min_value=0,
                step=500,
                value=user_budget.get('savings_target', 3000) if user_budget else 3000
            )
            
            st.markdown("### Category Allocation (%)")
            
            default_categories = user_budget.get('categories', {
                "Food & Dining": 0.3,
                "Rent": 0.4,
                "Transportation": 0.1,
                "Shopping": 0.1,
                "Others": 0.1
            })
            
            food_pct = st.slider(
                "Food & Dining",
                min_value=0,
                max_value=100,
                value=int(default_categories.get("Food & Dining", 0.3) * 100)
            )
            
            rent_pct = st.slider(
                "Rent",
                min_value=0,
                max_value=100,
                value=int(default_categories.get("Rent", 0.4) * 100)
            )
            
            transport_pct = st.slider(
                "Transportation",
                min_value=0,
                max_value=100,
                value=int(default_categories.get("Transportation", 0.1) * 100)
            )
            
            shopping_pct = st.slider(
                "Shopping",
                min_value=0,
                max_value=100,
                value=int(default_categories.get("Shopping", 0.1) * 100)
            )
            
            others_pct = st.slider(
                "Others",
                min_value=0,
                max_value=100,
                value=int(default_categories.get("Others", 0.1) * 100)
            )
            
            total_pct = food_pct + rent_pct + transport_pct + shopping_pct + others_pct
            
            if total_pct != 100:
                st.warning(f"Total allocation should be 100%. Currently: {total_pct}%")
            
            submitted = st.form_submit_button("Save Budget", use_container_width=True)
            
            if submitted:
                if total_pct != 100:
                    st.error("Total category allocation must equal 100%")
                else:
                    # Create or update budget
                    new_budget = {
                        "username": st.session_state.username,
                        "monthly_budget": monthly_budget,
                        "savings_target": savings_target,
                        "categories": {
                            "Food & Dining": food_pct / 100,
                            "Rent": rent_pct / 100,
                            "Transportation": transport_pct / 100,
                            "Shopping": shopping_pct / 100,
                            "Others": others_pct / 100
                        }
                    }
                    
                    if user_budget:
                        # Update existing budget
                        for i, budget in enumerate(budget_data):
                            if budget.get('username') == st.session_state.username:
                                budget_data[i] = new_budget
                                break
                    else:
                        # Add new budget
                        budget_data.append(new_budget)
                        # Award points for first budget
                        st.session_state.points += 20
                    
                    save_budget_data(budget_data)
                    st.success("Budget saved successfully!")
                    st.rerun()
        
        # Humorous budgeting tips
        st.markdown("---")
        st.markdown("### 💡 Budget Tips")
        tips = [
            "**50-30-20 Rule:** Allocate 50% for needs, 30% for wants, and 20% for savings and investments.",
            "**Zero-Based Budget:** Give every rupee a job. Make sure your income minus expenses equals zero.",
            "**The Envelope Method:** Use digital 'envelopes' for different spending categories. When it's empty, stop spending!"
        ]
        
        tip_idx = random.randint(0, len(tips) - 1)
        st.info(tips[tip_idx])

def show_investments():
    st.title("Investment Planner")
    
    tab1, tab2, tab3 = st.tabs(["Investment Calculator", "My Investments", "Investment Tips"])
    
    with tab1:
        st.subheader("SIP Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_investment = st.number_input(
                "Monthly Investment (₹)",
                min_value=500,
                step=500,
                value=5000
            )
            
            investment_period = st.slider(
                "Investment Period (Years)",
                min_value=1,
                max_value=30,
                value=10
            )
        
        with col2:
            expected_return_rate = st.slider(
                "Expected Annual Return (%)",
                min_value=1,
                max_value=30,
                value=12
            )
            
            inflation_rate = st.slider(
                "Expected Inflation Rate (%)",
                min_value=0,
                max_value=15,
                value=6
            )
        
        # Calculate SIP returns
        total_investment = monthly_investment * 12 * investment_period
        
        # Use the investment calculator to calculate returns
        years, invested_amount, expected_amount, inflation_adjusted = calculate_sip_returns(
            monthly_investment, investment_period, expected_return_rate, inflation_rate
        )
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Investment", f"₹{total_investment:,}")
        
        with col2:
            st.metric("Expected Returns", f"₹{expected_amount[-1]:,}")
        
        with col3:
            real_returns = expected_amount[-1] - total_investment
            st.metric("Wealth Gained", f"₹{real_returns:,}")
        
        # Plot the growth
        st.subheader("Investment Growth Over Time")
        
        growth_df = pd.DataFrame({
            'Year': years,
            'Invested Amount': invested_amount,
            'Expected Returns': expected_amount,
            'Inflation Adjusted': inflation_adjusted
        })
        
        fig = px.line(
            growth_df,
            x='Year',
            y=['Invested Amount', 'Expected Returns', 'Inflation Adjusted'],
            title="Investment Growth Projection",
            labels={'value': 'Amount (₹)', 'variable': 'Type'}
        )
        
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Lumpsum calculator
        st.subheader("Lumpsum Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            lumpsum_investment = st.number_input(
                "One-time Investment (₹)",
                min_value=1000,
                step=1000,
                value=100000
            )
            
            lumpsum_period = st.slider(
                "Investment Period (Years)",
                min_value=1,
                max_value=30,
                value=5,
                key="lumpsum_period"
            )
        
        with col2:
            lumpsum_return_rate = st.slider(
                "Expected Annual Return (%)",
                min_value=1,
                max_value=30,
                value=12,
                key="lumpsum_return"
            )
            
            lumpsum_inflation = st.slider(
                "Expected Inflation Rate (%)",
                min_value=0,
                max_value=15,
                value=6,
                key="lumpsum_inflation"
            )
        
        # Calculate lumpsum returns
        years, expected_amount, inflation_adjusted = calculate_lumpsum_returns(
            lumpsum_investment, lumpsum_period, lumpsum_return_rate, lumpsum_inflation
        )
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Initial Investment", f"₹{lumpsum_investment:,}")
        
        with col2:
            st.metric("Expected Value", f"₹{expected_amount[-1]:,}")
        
        with col3:
            real_returns = expected_amount[-1] - lumpsum_investment
            st.metric("Wealth Gained", f"₹{real_returns:,}")
        
        # Plot the growth
        lumpsum_df = pd.DataFrame({
            'Year': years,
            'Initial Investment': [lumpsum_investment] * len(years),
            'Expected Returns': expected_amount,
            'Inflation Adjusted': inflation_adjusted
        })
        
        fig = px.line(
            lumpsum_df,
            x='Year',
            y=['Initial Investment', 'Expected Returns', 'Inflation Adjusted'],
            title="Lumpsum Investment Growth Projection",
            labels={'value': 'Amount (₹)', 'variable': 'Type'}
        )
        
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Save calculation as investment
        with st.expander("Save This Calculation"):
            investment_name = st.text_input("Investment Name", placeholder="e.g., My SIP Plan")
            investment_type = st.selectbox("Investment Type", ["SIP", "Lumpsum"])
            
            if st.button("Save Investment Plan", use_container_width=True):
                if investment_name:
                    # Get investment data
                    investment_data = get_investment_data()
                    
                    # Create new investment
                    new_investment = {
                        "username": st.session_state.username,
                        "name": investment_name,
                        "type": investment_type,
                        "amount": monthly_investment if investment_type == "SIP" else lumpsum_investment,
                        "period": investment_period if investment_type == "SIP" else lumpsum_period,
                        "return_rate": expected_return_rate if investment_type == "SIP" else lumpsum_return_rate,
                        "created_date": datetime.now().strftime("%Y-%m-%d"),
                        "id": str(random.randint(10000, 99999)),
                        "growth": real_returns
                    }
                    
                    investment_data.append(new_investment)
                    save_investment_data(investment_data)
                    
                    # Award points
                    st.session_state.points += 15
                    
                    st.success("Investment plan saved successfully! You earned 15 points.")
                    st.rerun()
                else:
                    st.error("Please enter an investment name")
    
    with tab2:
        st.subheader("My Investment Plans")
        
        # Get investment data
        investment_data = get_investment_data()
        user_investments = [inv for inv in investment_data if inv.get('username') == st.session_state.username]
        
        if user_investments:
            # Calculate totals
            total_sip = sum(inv.get('amount', 0) for inv in user_investments if inv.get('type') == 'SIP')
            total_lumpsum = sum(inv.get('amount', 0) for inv in user_investments if inv.get('type') == 'Lumpsum')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total SIP Investment", f"₹{total_sip:,}/month")
            
            with col2:
                st.metric("Total Lumpsum Investment", f"₹{total_lumpsum:,}")
            
            # List all investments
            for investment in user_investments:
                with st.expander(f"{investment.get('name', 'Investment Plan')} ({investment.get('type', 'SIP')})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Type:** {investment.get('type', 'SIP')}")
                        st.markdown(f"**Amount:** ₹{investment.get('amount', 0):,}" + 
                                   ("/month" if investment.get('type') == 'SIP' else ""))
                        st.markdown(f"**Period:** {investment.get('period', 0)} years")
                    
                    with col2:
                        st.markdown(f"**Expected Return:** {investment.get('return_rate', 0)}%")
                        st.markdown(f"**Created Date:** {investment.get('created_date', '')}")
                        st.markdown(f"**Projected Growth:** ₹{investment.get('growth', 0):,}")
                    
                    if st.button("Delete", key=f"delete_inv_{investment.get('id', '')}"):
                        # Remove the investment
                        investment_data = [inv for inv in investment_data if inv.get('id') != investment.get('id', '')]
                        save_investment_data(investment_data)
                        st.success("Investment plan deleted successfully!")
                        st.rerun()
        else:
            st.info("You haven't saved any investment plans yet. Use the calculator to create and save your first plan.")
            
            # Humorous investment tip
            st.markdown("""
            > 🧠 **Investment Wisdom:** Remember, investing is like planting a tree. The best time to start was 20 years ago. 
            > The second best time is now! Create your first investment plan above.
            """)
    
    with tab3:
        st.subheader("Investment Tips for Beginners")
        
        tips = [
            {
                "title": "Start Early, Even with Small Amounts",
                "description": "The magic of compounding works best over longer periods. Even ₹500 a month can grow significantly over decades.",
                "emoji": "🌱"
            },
            {
                "title": "Understand the Power of SIP",
                "description": "Systematic Investment Plans (SIPs) allow you to invest fixed amounts regularly, reducing the impact of market volatility through rupee cost averaging.",
                "emoji": "⏱️"
            },
            {
                "title": "Diversify Your Investments",
                "description": "Don't put all your eggs in one basket. Spread your investments across different asset classes like equity, debt, gold, etc.",
                "emoji": "🧩"
            },
            {
                "title": "Know Your Risk Tolerance",
                "description": "Understand how much risk you're comfortable with. Higher returns usually come with higher risks.",
                "emoji": "⚖️"
            },
            {
                "title": "Have an Emergency Fund First",
                "description": "Before investing for long-term goals, build an emergency fund that covers 3-6 months of expenses.",
                "emoji": "🛡️"
            }
        ]
        
        for i, tip in enumerate(tips):
            with st.expander(f"{tip['emoji']} {tip['title']}"):
                st.markdown(tip['description'])
                
                # Add a fun fact or humorous note
                fun_facts = [
                    "**Fun Fact:** If you had invested ₹10,000 in Infosys in 1993, it would be worth over ₹5 crores today! Talk about a glow-up! 💅",
                    "**Friendly Reminder:** The stock market is the only store where people run away when there's a sale! 🏃‍♂️",
                    "**Pro Tip:** Checking your investments daily is like watching a plant grow - you'll drive yourself crazy! Check quarterly instead. 🌿",
                    "**Investment Truth:** Your salary is your active income. Your investments are your employees working while you sleep! 💤",
                    "**Money Wisdom:** Saving money is like losing weight. It's simple but not easy, and everyone has advice about it! 🏋️‍♀️"
                ]
                
                st.info(fun_facts[i % len(fun_facts)])
        
        # Gamified investment quiz
        st.subheader("Test Your Investment Knowledge")
        
        with st.form("investment_quiz"):
            st.markdown("Answer these questions to earn points and unlock achievements!")
            
            q1 = st.radio(
                "1. Which investment option typically provides the highest returns over the long term?",
                ["Fixed Deposits", "Equity/Stocks", "Savings Account", "Gold"]
            )
            
            q2 = st.radio(
                "2. What is the main advantage of a SIP (Systematic Investment Plan)?",
                ["Guaranteed returns", "Government backing", "Rupee cost averaging", "Tax exemption"]
            )
            
            q3 = st.radio(
                "3. Which of these is NOT a good investment practice?",
                ["Diversification", "Investing with a long-term horizon", "Timing the market", "Regular investing"]
            )
            
            submitted = st.form_submit_button("Submit Quiz")
            
            if submitted:
                score = 0
                
                if q1 == "Equity/Stocks":
                    score += 1
                
                if q2 == "Rupee cost averaging":
                    score += 1
                
                if q3 == "Timing the market":
                    score += 1
                
                st.success(f"You scored {score}/3 in the investment quiz!")
                
                # Award points based on score
                points_earned = score * 10
                st.session_state.points += points_earned
                
                st.markdown(f"🎉 You earned {points_earned} points!")
                
                # Check for achievement
                if score == 3:
                    achievement = "Investment Guru 🧠"
                    if achievement not in st.session_state.achievements:
                        st.session_state.achievements.append(achievement)
                        st.balloons()
                        st.success(f"🏆 Achievement unlocked: {achievement}")

def show_financial_assistant():
    st.title("Financial Assistant")
    
    tabs = st.tabs(["Ask Questions", "Financial Tips", "Financial Health Score"])
    
    with tabs[0]:
        st.subheader("Ask Your Financial Questions")
        
        question = st.text_input("Type your question here", placeholder="e.g., How can I save more money as a student?")
        
        if st.button("Get Answer", use_container_width=True):
            if question:
                # Example answers based on common financial questions
                answers = {
                    "save": "**Saving Money as a Student:**\n\n"
                           "1. **Track Your Expenses:** Use FinSmart's expense tracker to see where your money goes.\n"
                           "2. **Create a Budget:** Set realistic limits for different spending categories.\n"
                           "3. **Cook at Home:** Eating out can be expensive. Learn some basic cooking skills.\n"
                           "4. **Use Student Discounts:** Many places offer student discounts - always ask!\n"
                           "5. **Buy Used Textbooks:** Or borrow from the library instead of buying new.\n\n"
                           "**Humorous Tip:** Think of saving money like putting your wallet on a diet - a little discipline now means more freedom later! 💪",
                    
                    "invest": "**Investment Tips for Beginners:**\n\n"
                             "1. **Start Small:** Begin with small amounts that you're comfortable with.\n"
                             "2. **Use SIPs:** Systematic Investment Plans allow you to invest regularly without timing the market.\n"
                             "3. **Consider Index Funds:** They offer diversification with lower fees.\n"
                             "4. **Learn Before You Earn:** Educate yourself about investing basics.\n"
                             "5. **Be Patient:** Investing is a marathon, not a sprint.\n\n"
                             "**Fun Fact:** Warren Buffett made 99% of his wealth after his 50th birthday. It's never too late to start! 🚀",
                    
                    "budget": "**Effective Budgeting for Students:**\n\n"
                              "1. **Use the 50-30-20 Rule:** 50% for needs, 30% for wants, 20% for savings.\n"
                              "2. **Track Every Expense:** Use FinSmart to record all spending.\n"
                              "3. **Plan for Irregular Expenses:** Set aside money for upcoming events.\n"
                              "4. **Review Regularly:** Adjust your budget monthly based on your actual spending.\n"
                              "5. **Reward Yourself:** Include some fun money in your budget.\n\n"
                              "**Humorous Tip:** Budgeting is like a diet for your wallet - you can have the occasional treat, but don't make it a habit! 🍩",
                    
                    "loan": "**Student Loan Advice:**\n\n"
                           "1. **Understand the Terms:** Know your interest rates and repayment options.\n"
                           "2. **Pay More Than Minimum:** Even small extra payments can reduce total interest significantly.\n"
                           "3. **Explore Loan Forgiveness:** Check if your career qualifies for any loan forgiveness programs.\n"
                           "4. **Refinance if Possible:** Look for better interest rates after graduation.\n"
                           "5. **Avoid Additional Debt:** Don't add to your burden with credit card debt.\n\n"
                           "**Humorous Tip:** Student loans are like that friend who always remembers when you borrowed money - they never forget! 💸",
                    
                    "credit": "**Building Good Credit as a Student:**\n\n"
                             "1. **Get a Secured Credit Card:** Start with a low limit and always pay on time.\n"
                             "2. **Pay Bills on Time:** Late payments hurt your credit score.\n"
                             "3. **Keep Utilization Low:** Use less than 30% of your available credit.\n"
                             "4. **Don't Apply for Multiple Cards:** Too many applications can hurt your score.\n"
                             "5. **Monitor Your Credit Report:** Check for errors regularly.\n\n"
                             "**Humorous Tip:** Your credit score is like your financial reputation - it takes years to build and minutes to ruin, just like that one embarrassing dance video! 💃",
                }
                
                # Find the most relevant answer
                answer_key = None
                for key in answers:
                    if key in question.lower():
                        answer_key = key
                        break
                
                if answer_key:
                    st.markdown(answers[answer_key])
                else:
                    st.markdown("""
                    **General Financial Advice for Students:**
                    
                    1. **Track Your Spending:** You can't improve what you don't measure.
                    2. **Start Investing Early:** Even small amounts benefit from compound growth.
                    3. **Build an Emergency Fund:** Aim for 3-6 months of essential expenses.
                    4. **Limit Debt:** Avoid high-interest debt like credit cards.
                    5. **Develop Marketable Skills:** Invest in yourself to increase earning potential.
                    
                    **Humorous Tip:** Managing money is like juggling - it looks impossible until you learn it, then it's just regular dropping of balls! 🤹‍♂️
                    """)
                
                # Award points for engagement
                st.session_state.points += 2
                st.markdown("*You earned 2 points for asking a question!* 🌟")
            else:
                st.warning("Please enter a question first.")
    
    with tabs[1]:
        st.subheader("Daily Financial Tips")
        
        # List of financial tips with humorous twists
        tips = [
            {
                "title": "The Coffee Conundrum",
                "description": "A ₹150 daily coffee adds up to ₹54,750 annually. That's enough for a budget vacation! Consider making coffee at home a few days a week.",
                "savings": "Potential Annual Savings: ₹27,375",
                "emoji": "☕"
            },
            {
                "title": "The 30-Day Rule",
                "description": "For non-essential purchases, wait 30 days before buying. If you still want it after 30 days, it might be worth it. Most impulse desires fade faster than that leftover pizza in your fridge!",
                "savings": "Potential Savings: Varies, but typically 20-30% of discretionary spending",
                "emoji": "⏳"
            },
            {
                "title": "The Subscription Audit",
                "description": "Review all your subscriptions monthly. Do you really need five streaming services? Unless you've mastered the art of watching five shows simultaneously, probably not!",
                "savings": "Potential Annual Savings: ₹3,600-12,000",
                "emoji": "📺"
            },
            {
                "title": "The 'Rupee Cost Averaging' Trick",
                "description": "Invest a fixed amount regularly regardless of market conditions. It's like dating - consistency matters more than perfect timing!",
                "savings": "Potential Benefit: Reduced risk and better long-term returns",
                "emoji": "📈"
            },
            {
                "title": "The 'Needs vs. Wants' Challenge",
                "description": "Before every purchase, ask: Is this a need or a want? If it's a want, how badly do you want it? On a scale from 'meh' to 'I've been dreaming about this since childhood'?",
                "savings": "Potential Savings: Up to 25% of monthly expenses",
                "emoji": "🛒"
            }
        ]
        
        # Display tips in expandable sections
        for tip in tips:
            with st.expander(f"{tip['emoji']} {tip['title']}"):
                st.markdown(tip['description'])
                st.markdown(f"**{tip['savings']}**")
                
                # Add a call-to-action button
                if st.button("I'll Try This!", key=f"tip_{tip['title']}"):
                    st.success("Great choice! You earned 5 points for committing to better financial habits.")
                    # Award points
                    st.session_state.points += 5
                    st.rerun()
        
        # Personalized tip based on user data
        st.subheader("Personalized Tip")
        
        # Get expense data
        expense_data = get_expense_data()
        user_expenses = [exp for exp in expense_data if exp.get('username') == st.session_state.username]
        
        if user_expenses:
            # Analyze spending patterns
            categories = {}
            for expense in user_expenses:
                category = expense.get('category', 'Others')
                amount = expense.get('amount', 0)
                categories[category] = categories.get(category, 0) + amount
            
            # Find highest spending category
            highest_category = max(categories.items(), key=lambda x: x[1]) if categories else (None, 0)
            
            if highest_category[0]:
                tips_by_category = {
                    "Food & Dining": "Your highest expense is on Food & Dining. Consider meal prepping on weekends - your wallet and waistline will thank you! Cooking at home can save up to 70% compared to eating out.",
                    "Rent": "Rent is your biggest expense. While you can't eliminate it, consider if having a roommate or moving to a slightly less expensive area might work for you. A 10% rent reduction adds up significantly over a year!",
                    "Transportation": "You spend a lot on transportation. Consider carpooling, using public transport, or embracing your inner fitness guru by walking or cycling for short distances. Your heart and wallet will both get stronger!",
                    "Shopping": "Shopping seems to be your weakness. Try the 24-hour rule: leave items in your cart for 24 hours before purchasing. Most impulse buys won't pass this test!",
                    "Education": "While education is an investment, look for free or discounted learning resources. Many universities offer free courses online, and libraries are basically free knowledge buffets!",
                    "Entertainment": "Entertainment is your top expense. Try free alternatives like community events, nature walks, or that novel that's been collecting dust on your shelf. The best memories often come from the least expensive activities!"
                }
                
                tip = tips_by_category.get(highest_category[0], "Look for ways to reduce spending in your highest category. Small changes add up to big savings over time!")
                
                st.info(f"💡 **Based on your spending pattern:** {tip}")
        else:
            st.info("Add your expenses to get personalized financial tips!")
    
    with tabs[2]:
        st.subheader("Financial Health Score")
        
        # Get user data
        expense_data = get_expense_data()
        budget_data = get_budget_data()
        investment_data = get_investment_data()
        
        user_expenses = [exp for exp in expense_data if exp.get('username') == st.session_state.username]
        user_budget = next((b for b in budget_data if b.get('username') == st.session_state.username), None)
        user_investments = [inv for inv in investment_data if inv.get('username') == st.session_state.username]
        
        # Calculate score components
        budget_score = 0
        expense_score = 0
        investment_score = 0
        savings_score = 0
        
        # Budget score (max 25 points)
        if user_budget:
            budget_score = 25
        
        # Expense tracking score (max 25 points)
        if user_expenses:
            # Award points based on consistency of tracking
            days_tracked = len(set(exp.get('date', '') for exp in user_expenses))
            current_month = datetime.now().strftime("%Y-%m")
            month_expenses = [exp for exp in user_expenses if exp.get('date', '').startswith(current_month)]
            
            if days_tracked > 20:
                expense_score = 25
            elif days_tracked > 10:
                expense_score = 15
            elif days_tracked > 0:
                expense_score = 10
            
            # Bonus for tracking in current month
            if len(month_expenses) > 0:
                expense_score = min(25, expense_score + 5)
        
        # Investment score (max 25 points)
        if user_investments:
            investment_count = len(user_investments)
            investment_score = min(25, investment_count * 5)
        
        # Savings score (max 25 points)
        if user_budget and user_expenses:
            monthly_budget = user_budget.get('monthly_budget', 10000)
            savings_target = user_budget.get('savings_target', 3000)
            
            # Calculate monthly expenses
            current_month = datetime.now().strftime("%Y-%m")
            monthly_expenses = sum(exp.get('amount', 0) for exp in user_expenses 
                                  if exp.get('date', '').startswith(current_month))
            
            # Calculate savings rate
            if monthly_expenses < monthly_budget:
                actual_savings = monthly_budget - monthly_expenses
                savings_rate = actual_savings / monthly_budget if monthly_budget else 0
                
                if savings_rate >= 0.2:  # Saving 20% or more
                    savings_score = 25
                elif savings_rate >= 0.1:  # Saving 10-20%
                    savings_score = 20
                elif savings_rate > 0:  # Saving something
                    savings_score = 15
            else:
                savings_score = 0
        
        # Calculate total score
        total_score = budget_score + expense_score + investment_score + savings_score
        
        # Display score
        st.markdown(f"### Your Financial Health Score: {total_score}/100")
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = total_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Financial Health"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#4CAF50" if total_score >= 70 else "#FFC107" if total_score >= 40 else "#F44336"},
                'steps': [
                    {'range': [0, 40], 'color': "lightgray"},
                    {'range': [40, 70], 'color': "gray"},
                    {'range': [70, 100], 'color': "darkgray"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': total_score
                }
            }
        ))
        
        fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Score breakdown
        st.markdown("### Score Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Budget Planning:** {budget_score}/25")
            st.progress(budget_score/25)
            
            st.markdown(f"**Expense Tracking:** {expense_score}/25")
            st.progress(expense_score/25)
        
        with col2:
            st.markdown(f"**Investment Planning:** {investment_score}/25")
            st.progress(investment_score/25)
            
            st.markdown(f"**Savings Rate:** {savings_score}/25")
            st.progress(savings_score/25)
        
        # Recommendations
        st.markdown("### Recommendations to Improve Your Score")
        
        recommendations = []
        
        if budget_score < 25:
            recommendations.append("🎯 **Create a Budget:** Set up a monthly budget to plan your spending and saving.")
        
        if expense_score < 25:
            recommendations.append("📝 **Track Expenses Regularly:** Record your expenses daily to maintain awareness of your spending patterns.")
        
        if investment_score < 25:
            recommendations.append("💰 **Start Investing:** Set up SIPs or small investments to begin your wealth creation journey.")
        
        if savings_score < 25:
            recommendations.append("🏦 **Increase Savings Rate:** Aim to save at least 20% of your income by reducing non-essential expenses.")
        
        if not recommendations:
            st.success("Great job! You're already demonstrating excellent financial management habits.")
        else:
            for recommendation in recommendations:
                st.markdown(recommendation)
        
        # Humorous financial advice
        st.markdown("---")
        st.markdown("### 💡 Funny Financial Wisdom")
        
        quotes = [
            "\"A budget is telling your money where to go instead of wondering where it went.\" - Dave Ramsey",
            "\"Money is a terrible master but an excellent servant.\" - P.T. Barnum",
            "\"The stock market is filled with individuals who know the price of everything, but the value of nothing.\" - Phillip Fisher",
            "\"It's not your salary that makes you rich, it's your spending habits.\" - Charles A. Jaffe",
            "\"Investing should be more like watching paint dry or watching grass grow. If you want excitement, take Rs.800 and go to Goa.\" - Paul Samuelson (Modified)"
        ]
        
        st.info(random.choice(quotes))

# Main function to run the app
def main():
    if not st.session_state.login_status:
        show_login_page()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
