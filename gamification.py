def get_achievement(points):
    """
    Return an achievement based on points
    """
    achievements = {
        100: "Financial Novice: Started your financial journey!",
        200: "Budget Master: Created your first budget plan!",
        300: "Expense Tracker: Consistently tracking your spending!",
        500: "Savings Hero: Building your financial cushion!",
        750: "Investment Beginner: Made your first investment plan!",
        1000: "Financial Wizard: Managing your money like a pro!",
        1500: "Money Guru: Teaching others about financial wisdom!",
        2000: "Wealth Architect: Building a solid financial future!",
        3000: "Financial Freedom Fighter: On your way to independence!",
        5000: "FinSmart Legend: Achieved legendary financial status!"
    }
    
    # Find the highest achievement unlocked
    unlocked_achievement = None
    for threshold, achievement in sorted(achievements.items()):
        if points >= threshold:
            unlocked_achievement = achievement
    
    return unlocked_achievement

def update_points(current_points):
    """
    Check if new achievement is unlocked based on points
    Returns the achievement if newly unlocked, None otherwise
    """
    achievements = {
        100: "Financial Novice",
        200: "Budget Master",
        300: "Expense Tracker",
        500: "Savings Hero",
        750: "Investment Beginner",
        1000: "Financial Wizard",
        1500: "Money Guru",
        2000: "Wealth Architect",
        3000: "Financial Freedom Fighter",
        5000: "FinSmart Legend"
    }
    
    # Find the next achievement that could be unlocked
    for threshold, achievement in sorted(achievements.items()):
        if current_points >= threshold and current_points - 10 < threshold:  # Assuming points are added in increments of at least 5
            return achievement
    
    return None

def get_level(points):
    """
    Return user level based on points
    """
    levels = [
        (0, "Beginner"),
        (250, "Apprentice"),
        (500, "Intermediate"),
        (1000, "Advanced"),
        (2000, "Expert"),
        (5000, "Master")
    ]
    
    current_level = "Beginner"
    for threshold, level in levels:
        if points >= threshold:
            current_level = level
    
    return current_level

def get_next_level_threshold(points):
    """
    Return points needed for next level
    """
    levels = [
        (0, "Beginner"),
        (250, "Apprentice"),
        (500, "Intermediate"),
        (1000, "Advanced"),
        (2000, "Expert"),
        (5000, "Master")
    ]
    
    for threshold, _ in levels:
        if points < threshold:
            return threshold
    
    return None  # Already at max level

def calculate_streak(user_expenses):
    """
    Calculate the current streak of days with expense tracking
    """
    if not user_expenses:
        return 0
    
    # Sort expenses by date
    from datetime import datetime, timedelta
    
    dates = [exp.get('date', '') for exp in user_expenses]
    valid_dates = []
    
    for date_str in dates:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            valid_dates.append(date_obj)
        except:
            continue
    
    if not valid_dates:
        return 0
    
    # Get unique dates
    unique_dates = list(set(valid_dates))
    unique_dates.sort(reverse=True)
    
    # Calculate streak
    streak = 1
    today = datetime.now().date()
    
    # Check if tracked today
    if not any(d.date() == today for d in unique_dates):
        return 0
    
    # Check consecutive days
    for i in range(1, len(unique_dates)):
        prev_date = unique_dates[i-1].date()
        curr_date = unique_dates[i].date()
        
        if prev_date - curr_date == timedelta(days=1):
            streak += 1
        else:
            break
    
    return streak

def get_badge(category, value):
    """
    Return badge based on category and value
    """
    badges = {
        "expense_tracker": {
            10: "Expense Tracking Novice",
            30: "Expense Tracking Enthusiast",
            60: "Expense Master",
            90: "Expense Tracking Guru",
            180: "Expense Tracking Legend"
        },
        "budget_adherence": {
            70: "Budget Follower",
            80: "Budget Keeper",
            90: "Budget Master",
            95: "Budget Expert",
            99: "Budget Wizard"
        },
        "savings_rate": {
            10: "Saver Novice",
            20: "Consistent Saver",
            30: "Super Saver",
            40: "Savings Champion",
            50: "Savings Legend"
        },
        "investment_count": {
            1: "First-time Investor",
            3: "Portfolio Builder",
            5: "Investment Enthusiast",
            10: "Investment Master",
            15: "Investment Guru"
        }
    }
    
    category_badges = badges.get(category, {})
    earned_badge = None
    
    for threshold, badge in sorted(category_badges.items()):
        if value >= threshold:
            earned_badge = badge
    
    return earned_badge
