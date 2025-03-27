import numpy as np

def calculate_sip_returns(monthly_investment, years, expected_return_rate, inflation_rate=6):
    """
    Calculate SIP (Systematic Investment Plan) returns with inflation adjustment
    
    Parameters:
    monthly_investment (float): Monthly investment amount
    years (int): Investment period in years
    expected_return_rate (float): Expected annual return rate in percentage
    inflation_rate (float): Expected annual inflation rate in percentage
    
    Returns:
    tuple: (years, invested_amount, expected_amount, inflation_adjusted)
    """
    # Monthly rate (compounded monthly)
    monthly_rate = expected_return_rate / 100 / 12
    inflation_monthly = inflation_rate / 100 / 12
    
    # Total number of months
    months = years * 12
    
    # Initialize arrays
    years_array = np.arange(1, years + 1)
    invested_amount = np.zeros(years)
    expected_amount = np.zeros(years)
    inflation_adjusted = np.zeros(years)
    
    # Calculate for each year
    for i in range(years):
        months_completed = (i + 1) * 12
        
        # Amount invested till this year
        invested_amount[i] = monthly_investment * months_completed
        
        # Calculate expected return using FV of SIP formula
        expected_amount[i] = monthly_investment * ((pow(1 + monthly_rate, months_completed) - 1) / monthly_rate) * (1 + monthly_rate)
        
        # Adjust for inflation
        inflation_adjustment = pow(1 + inflation_monthly, months_completed)
        inflation_adjusted[i] = expected_amount[i] / inflation_adjustment
    
    return years_array, invested_amount, expected_amount, inflation_adjusted

def calculate_lumpsum_returns(investment_amount, years, expected_return_rate, inflation_rate=6):
    """
    Calculate lumpsum investment returns with inflation adjustment
    
    Parameters:
    investment_amount (float): One-time investment amount
    years (int): Investment period in years
    expected_return_rate (float): Expected annual return rate in percentage
    inflation_rate (float): Expected annual inflation rate in percentage
    
    Returns:
    tuple: (years, expected_amount, inflation_adjusted)
    """
    # Annual rates
    annual_rate = expected_return_rate / 100
    inflation_annual = inflation_rate / 100
    
    # Initialize arrays
    years_array = np.arange(1, years + 1)
    expected_amount = np.zeros(years)
    inflation_adjusted = np.zeros(years)
    
    # Calculate for each year
    for i in range(years):
        year = i + 1
        
        # Calculate expected return using compound interest formula
        expected_amount[i] = investment_amount * pow(1 + annual_rate, year)
        
        # Adjust for inflation
        inflation_adjustment = pow(1 + inflation_annual, year)
        inflation_adjusted[i] = expected_amount[i] / inflation_adjustment
    
    return years_array, expected_amount, inflation_adjusted

def calculate_goal_sip(target_amount, years, expected_return_rate):
    """
    Calculate the required monthly SIP to reach a financial goal
    
    Parameters:
    target_amount (float): Target amount to achieve
    years (int): Investment period in years
    expected_return_rate (float): Expected annual return rate in percentage
    
    Returns:
    float: Required monthly SIP amount
    """
    # Monthly rate
    monthly_rate = expected_return_rate / 100 / 12
    
    # Total number of months
    months = years * 12
    
    # Calculate required monthly SIP using formula
    # M = P / [((1+r)^n - 1) / r) * (1+r)]
    # Where:
    # M = Monthly SIP amount
    # P = Target amount
    # r = Monthly interest rate
    # n = Number of months
    
    denominator = ((pow(1 + monthly_rate, months) - 1) / monthly_rate) * (1 + monthly_rate)
    required_sip = target_amount / denominator
    
    return required_sip

def calculate_investment_duration(monthly_investment, target_amount, expected_return_rate):
    """
    Calculate the time required to reach a financial goal with regular SIP
    
    Parameters:
    monthly_investment (float): Monthly investment amount
    target_amount (float): Target amount to achieve
    expected_return_rate (float): Expected annual return rate in percentage
    
    Returns:
    float: Required time in years
    """
    # Monthly rate
    monthly_rate = expected_return_rate / 100 / 12
    
    # Using the formula: P = M * [((1+r)^n - 1) / r) * (1+r)]
    # We need to solve for n (number of months)
    # This is approximated using logarithms
    
    numerator = target_amount * monthly_rate
    denominator = monthly_investment * (1 + monthly_rate)
    
    # Calculate number of months using approximation
    months = np.log(1 + (numerator / denominator)) / np.log(1 + monthly_rate)
    
    # Convert to years
    years = months / 12
    
    return years
