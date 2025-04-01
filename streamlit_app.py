import streamlit as st
import numpy as np
import math
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="Finance Advisor", page_icon="💰", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
        .main { background-color: #111; color: #fff; }
        div.block-container { padding: 2rem; }
        .stButton>button { width: 100%; }
        h1, h2, h3 { text-align: center; color: #FFD700; }
        .score { font-size: 28px; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>💰 Finance Advisor</h1>", unsafe_allow_html=True)
st.markdown("<h3>Your Personal Financial Dashboard</h3>", unsafe_allow_html=True)

# --- Sidebar (User Inputs) ---
st.sidebar.header("📊 User Input")
income = st.sidebar.number_input("💵 Monthly Income (Before Taxes): $", min_value=0.0, format="%.2f")
expenses = st.sidebar.number_input("💸 Monthly Expenses (Including Taxes): $", min_value=0.0, format="%.2f")
savings = st.sidebar.number_input("🏦 Total Savings: $", min_value=0.0, format="%.2f")
investments = st.sidebar.number_input("📈 Total Investments: $", min_value=0.0, format="%.2f")
debt = st.sidebar.number_input("💳 Current Debt ($):", min_value=0.0, format="%.2f")
assets = st.sidebar.number_input("🏡 Total Asset Value ($):", min_value=0.0, format="%.2f")
age = st.sidebar.number_input("🎂 Age:", min_value=10, max_value=100, step=1)
credit_score = st.sidebar.slider("📊 Credit Score (300-850):", min_value=300, max_value=850, value=700)

st.sidebar.header("🧾 Tax Rates")
federal_tax = st.sidebar.slider("Federal Tax Rate (%)", 0, 50, 15)
state_tax = st.sidebar.slider("State Tax Rate (%)", 0, 50, 5)
local_tax = st.sidebar.slider("Local Tax Rate (%)", 0, 50, 3)

# --- Financial Calculations ---
net_income = income * (1 - (federal_tax + state_tax + local_tax) / 100)
net_worth = assets + savings + investments - debt
debt_to_income_ratio = (debt / income * 100) if income > 0 else 0
savings_rate = (savings / (income * 12)) if income > 0 else 0
investment_rate = (investments / (income * 12)) if income > 0 else 0

# --- Emergency Fund Calculation (Capped at 6 Months) ---
emergency_fund_cap = 6  
emergency_fund = min(savings / (expenses / 12), emergency_fund_cap) if expenses > 0 else float('inf')
needed_savings_for_fund = max(0, (expenses / 12) * emergency_fund_cap - savings)
savings_contribution = min(needed_savings_for_fund * 0.3, savings) if needed_savings_for_fund > 0 else 0

# --- Financial Grading System (0-100) ---
score = 100  
if debt_to_income_ratio > 40:
    score -= 20  
if savings_rate < 0.15:
    score -= 15  
if emergency_fund < 3:
    score -= 10  
if investment_rate < 0.2:
    score -= 10  
if credit_score < 600:
    score -= 20  

grade_color = "green" if score > 75 else "yellow" if score > 50 else "red"

# --- Financial Advice ---
def get_advice():
    advice = []
    if debt_to_income_ratio > 40:
        advice.append("⚠️ Your Debt-to-Income Ratio is **high!** Reduce debt.")
    if savings_rate < 0.15:
        advice.append("📉 Your savings rate is **below 15%**. Consider increasing savings.")
    if emergency_fund < 3:
        advice.append("🛑 You need at least 3 months of savings in your emergency fund.")
    if investment_rate < 0.2:
        advice.append("💡 Increase your investments for long-term financial security.")
    if credit_score < 600:
        advice.append("📉 Improve your **credit score** to access better financial options.")
    
    return advice if advice else ["✅ Your finances are in great shape! Keep it up!"]

advice = get_advice()

# --- Display Financial Overview ---
st.subheader("📊 Your Financial Overview")
st.markdown(f"**💰 Net Monthly Income:** `${net_income:,.2f}`")
st.markdown(f"**📈 Net Worth:** `${net_worth:,.2f}`")
st.markdown(f"**💳 Debt-to-Income Ratio:** `{debt_to_income_ratio:.2f}%`")
st.markdown(f"**🚨 Emergency Fund:** `{emergency_fund:.2f}` months of expenses")

# --- Financial Score ---
st.markdown(f"<p class='score' style='color:{grade_color};'>💯 Financial Score: {score}/100</p>", unsafe_allow_html=True)

st.subheader("📌 Personalized Financial Advice")
for tip in advice:
    st.markdown(f"- {tip}")

# --- National Comparison Report (Percentiles) ---
st.subheader("📈 National Comparison Report (Lower is better)")

# National Data
national_avg_savings = 6000
national_avg_income = 4500
national_avg_debt = 30000
national_avg_credit = 710

# Percentile Calculations (lower is worse for savings, higher is worse for debt)
def calculate_percentile(value, national_avg, is_debt=False):
    if is_debt:
        return min(100, max(0, 100 - (value / national_avg) * 100))
    return min(100, max(0, (value / national_avg) * 100))

savings_percentile = calculate_percentile(savings, national_avg_savings)
income_percentile = calculate_percentile(income, national_avg_income)
debt_percentile = calculate_percentile(debt, national_avg_debt, is_debt=True)
credit_score_percentile = calculate_percentile(credit_score, national_avg_credit)

comparison_report = f"""
- **Savings:** You have `{savings:,.2f}`. Your savings are at the `{savings_percentile}th` percentile in the U.S.
- **Income:** Your income is `${income:,.2f}`. Your income is at the `{income_percentile}th` percentile in the U.S.
- **Debt:** Your debt is `${debt:,.2f}`. Your debt is at the `{debt_percentile}th` percentile in the U.S. (Higher is worse)
- **Credit Score:** Your score is `{credit_score}`. Your credit score is at the `{credit_score_percentile}th` percentile in the U.S.
"""
st.markdown(comparison_report)

# --- Data Visualization ---
st.subheader("📊 Financial Distribution")
fig = go.Figure(data=[go.Pie(
    labels=["Savings", "Investments", "Debt", "Assets"],
    values=[savings, investments, debt, assets],
    hole=0.4
)])
fig.update_layout(showlegend=True, width=600, height=400)
st.plotly_chart(fig, use_container_width=True)

# --- Financial Projections ---
def forecast_years(years):
    """Predict financial growth over time."""
    income_growth = 0.03
    savings_growth = 0.15
    investment_growth = 0.06
    debt_reduction = 0.05
    credit_score_improvement = 5

    future_income = income * ((1 + income_growth) ** years)
    future_savings = savings + (net_income * savings_growth * 12 * years)
    future_investments = investments * ((1 + investment_growth) ** years)
    future_debt = debt * ((1 - debt_reduction) ** years)
    future_credit_score = min(850, credit_score + (credit_score_improvement * years))
    future_net_worth = future_savings + future_investments - future_debt

    return {
        "Income": future_income,
        "Savings": future_savings,
        "Investments": future_investments,
        "Debt": future_debt,
        "Net Worth": future_net_worth,
        "Credit Score": future_credit_score
    }

st.subheader("🚀 Financial Projections")
projection_years = [2, 5, 10]
projection_data = {year: forecast_years(year) for year in projection_years}

for year in projection_years:
    st.markdown(f"### 📅 In {year} years:")
    st.markdown(f"- **💰 Income:** `${projection_data[year]['Income']:,.2f}`")
    st.markdown(f"- **🏦 Savings:** `${projection_data[year]['Savings']:,.2f}`")
    st.markdown(f"- **📈 Investments:** `${projection_data[year]['Investments']:,.2f}`")
    st.markdown(f"- **💳 Debt:** `${projection_data[year]['Debt']:,.2f}`")
    st.markdown(f"- **📊 Net Worth:** `${projection_data[year]['Net Worth']:,.2f}`")
    st.markdown(f"- **🏆 Credit Score:** `{projection_data[year]['Credit Score']}`")

st.markdown("---")
st.markdown("<h3>🔁 Come back anytime to track your progress!</h3>", unsafe_allow_html=True)

