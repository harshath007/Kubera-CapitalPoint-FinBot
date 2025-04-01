import numpy as np
import streamlit as st

def get_percentile(user_value, national_average, national_std_dev):
    """Calculate the percentile ranking of the user's value compared to national data."""
    if national_std_dev == 0:
        return 50  # If there's no variation, assume user is average
    z_score = (user_value - national_average) / national_std_dev
    percentile = round(100 * (1 - 0.5 * (1 + np.math.erf(z_score / np.sqrt(2)))), 2)
    return max(1, min(100, percentile))  # Ensure percentile stays between 1 and 100

def financial_report():
    st.set_page_config(page_title="Finance Advisor", page_icon="💰", layout="centered")
    st.title("💰 Finance Advisor")

    st.sidebar.header("User Input")
    
    # User inputs with validation
    income = st.sidebar.number_input("Monthly Income (Before Taxes): $", min_value=0.0, format="%.2f")
    expenses = st.sidebar.number_input("Monthly Expenses: $", min_value=0.0, format="%.2f")
    savings = st.sidebar.number_input("Total Savings: $", min_value=0.0, format="%.2f")
    investments = st.sidebar.number_input("Total Investments: $", min_value=0.0, format="%.2f")
    age = st.sidebar.number_input("Age: ", min_value=0)
    
    st.sidebar.markdown("**Tax Rates**")
    federal_tax = st.sidebar.number_input("Federal Tax Rate (%)", min_value=0.0, max_value=100.0)
    state_tax = st.sidebar.number_input("State Tax Rate (%)", min_value=0.0, max_value=100.0)
    local_tax = st.sidebar.number_input("Local Tax Rate (%)", min_value=0.0, max_value=100.0)
    
    credit_score = st.sidebar.number_input("Credit Score (300-850):", min_value=300, max_value=850)

    st.sidebar.markdown("**Financial Goals**")
    savings_goal = st.sidebar.number_input("Savings Goal ($):", min_value=0.0, format="%.2f")
    investment_goal = st.sidebar.number_input("Investment Goal ($):", min_value=0.0, format="%.2f")
    debt = st.sidebar.number_input("Current Debt ($):", min_value=0.0, format="%.2f")

    # National averages and standard deviations for comparison
    national_averages = {
        "income": 5000, "expenses": 3500, "savings": 25000, "investments": 40000,
        "credit_score": 710, "net_worth": 100000, "debt": 20000, "emergency_fund": 15000,
        "savings_rate": 0.15, "investment_rate": 0.2
    }
    national_std_dev = {
        "income": 2000, "expenses": 1500, "savings": 15000, "investments": 30000,
        "credit_score": 40, "net_worth": 50000, "debt": 10000, "emergency_fund": 8000,
        "savings_rate": 0.1, "investment_rate": 0.1
    }

    # Financial Calculations
    net_income = income * (1 - (federal_tax + state_tax + local_tax) / 100)
    net_worth = savings + investments
    debt_to_income_ratio = debt / income * 100  # Debt-to-income ratio as percentage
    emergency_fund = min(savings / (expenses / 12), 12)  # Capped at 12 months of expenses
    savings_rate = savings / (income * 12)
    investment_rate = investments / (income * 12)

    # Percentile Calculations
    percentiles = {
        "income": get_percentile(income, national_averages["income"], national_std_dev["income"]),
        "expenses": get_percentile(expenses, national_averages["expenses"], national_std_dev["expenses"]),
        "savings": get_percentile(savings, national_averages["savings"], national_std_dev["savings"]),
        "investments": get_percentile(investments, national_averages["investments"], national_std_dev["investments"]),
        "credit_score": get_percentile(credit_score, national_averages["credit_score"], national_std_dev["credit_score"]),
        "net_worth": get_percentile(net_worth, national_averages["net_worth"], national_std_dev["net_worth"]),
        "debt": get_percentile(debt, national_averages["debt"], national_std_dev["debt"]),
        "emergency_fund": get_percentile(emergency_fund, national_averages["emergency_fund"], national_std_dev["emergency_fund"]),
        "savings_rate": get_percentile(savings_rate, national_averages["savings_rate"], national_std_dev["savings_rate"]),
        "investment_rate": get_percentile(investment_rate, national_averages["investment_rate"], national_std_dev["investment_rate"])
    }

    # Age-based comparison
    national_net_worth_by_age = {20: 5000, 30: 35000, 40: 80000, 50: 150000, 60: 250000}
    closest_age = min(national_net_worth_by_age.keys(), key=lambda x: abs(x - age))
    age_comparison = get_percentile(net_worth, national_net_worth_by_age[closest_age], national_std_dev["net_worth"])

    # Financial Predictions (2, 5, 10 years)
    income_growth_rate = 0.03  # 3% annual growth in income
    savings_growth_rate = 0.15  # User saves 15% of net income
    investment_growth_rate = 0.06  # 6% annual return on investments
    debt_reduction_rate = 0.05  # Reduce debt by 5% per year
    credit_score_improvement = 5  # Improve credit score by 5 points per year

    def forecast_years(years):
        """Forecast the financial situation in the future (2, 5, 10 years)."""
        future_income = income * ((1 + income_growth_rate) ** years)
        future_savings = savings + (net_income * savings_growth_rate * 12 * years)
        future_investments = investments * ((1 + investment_growth_rate) ** years)
        future_debt = debt * ((1 - debt_reduction_rate) ** years)
        future_credit_score = credit_score + (credit_score_improvement * years)
        future_net_worth = future_savings + future_investments - future_debt
        future_emergency_fund = future_savings / (expenses / 12)  # Months worth of future savings
        
        return {
            "future_income": future_income,
            "future_savings": future_savings,
            "future_investments": future_investments,
            "future_debt": future_debt,
            "future_credit_score": future_credit_score,
            "future_net_worth": future_net_worth,
            "future_emergency_fund": future_emergency_fund
        }

    # Projections for 2, 5, and 10 years
    projections = {
        "2_years": forecast_years(2),
        "5_years": forecast_years(5),
        "10_years": forecast_years(10)
    }

    st.subheader("Your Financial Overview")
    st.markdown(f"**Net Monthly Income**: ${net_income:,.2f}")
    st.markdown(f"**Net Worth**: ${net_worth:,.2f}")
    st.markdown(f"**Emergency Fund**: {emergency_fund:.2f} months of expenses")
    st.markdown(f"**Debt-to-Income Ratio**: {debt_to_income_ratio:.2f}%")
    
    st.subheader("Percentiles Comparison")
    st.write("Here’s how your financial situation compares to the national averages:")
    for key, percentile in percentiles.items():
        st.write(f"{key.capitalize()}: **{percentile}th percentile**")
    
    st.write(f"**Your net worth compared to your age group**: {age_comparison}th percentile")

    st.subheader("Financial Projections")
    for period, data in projections.items():
        st.markdown(f"### In {period.replace('_', ' ').capitalize()}:")
        st.markdown(f"**Projected Income**: ${data['future_income']:,.2f}")
        st.markdown(f"**Projected Savings**: ${data['future_savings']:,.2f}")
        st.markdown(f"**Projected Investments**: ${data['future_investments']:,.2f}")
        st.markdown(f"**Projected Debt**: ${data['future_debt']:,.2f}")
        st.markdown(f"**Projected Credit Score**: {data['future_credit_score']}")
        st.markdown(f"**Projected Net Worth**: ${data['future_net_worth']:,.2f}")
        st.markdown(f"**Emergency Fund (Months)**: {data['future_emergency_fund']:.2f}")
        st.markdown("\n---")

if __name__ == "__main__":
    financial_report()

