import streamlit as st
import numpy as np
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
income = st.sidebar.number_input("💵 Monthly Income (Before Taxes): $", min_value=0.01, format="%.2f")
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
total_tax_rate = (federal_tax + state_tax + local_tax) / 100
net_income = income * (1 - total_tax_rate)
net_worth = assets + savings + investments - debt
debt_to_income_ratio = (debt / income * 100) if income > 0 else 0
savings_rate = (savings / (income * 12)) if income > 0 else 0
investment_rate = (investments / (income * 12)) if income > 0 else 0

# --- Emergency Fund Calculation ---
emergency_fund_cap = 6
emergency_fund = (savings / (expenses / 12)) if expenses > 0 else float('inf')
emergency_fund = min(emergency_fund, emergency_fund_cap)
needed_savings_for_fund = max(0, (expenses / 12) * emergency_fund_cap - savings)
savings_contribution = min(needed_savings_for_fund * 0.3, savings) if needed_savings_for_fund > 0 else 0

# --- Financial Score Calculation ---
score = 100
if debt_to_income_ratio > 40:
    score -= 15
if savings_rate < 0.15:
    score -= 10
if emergency_fund < 3:
    score -= 5
if investment_rate < 0.2:
    score -= 10
if credit_score < 600:
    score -= 10
if credit_score > 750:
    score += 5
if debt == 0:
    score += 10
if savings_rate > 0.3:
    score += 5
if investment_rate > 0.25:
    score += 5
score = max(0, min(score, 100))

# --- Display Financial Overview ---
st.subheader("📊 Your Financial Overview")
st.markdown(f"**💰 Net Monthly Income:** `${net_income:,.2f}`")
st.markdown(f"**📈 Net Worth:** `${net_worth:,.2f}`")
st.markdown(f"**💳 Debt-to-Income Ratio:** `{debt_to_income_ratio:.2f}%`")
st.markdown(f"**🚨 Emergency Fund:** `{emergency_fund:.2f}` months (Cap: 6 months)")
st.markdown(f"**💾 Emergency Fund Contribution:** `${savings_contribution:,.2f}`")

# --- Display Financial Score ---
st.markdown(f"<p class='score'>💯 Financial Score: {score}/100</p>", unsafe_allow_html=True)

# --- National Comparison ---
st.subheader("📊 National Comparison")
st.markdown("This section can be updated with real percentile data.")

# --- Visual Representation ---
st.subheader("📊 Financial Data Chart")
fig = go.Figure()
fig.add_trace(go.Bar(x=["Income", "Savings", "Investments", "Debt"], y=[income, savings, investments, debt], marker_color=["blue", "green", "orange", "red"]))
fig.update_layout(title="Your Financial Data", yaxis=dict(title="Amount ($)"))
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
    st.markdown(f"- **💰 Income:** ${projection_data[year]['Income']:,.2f}")
    st.markdown(f"- **🏦 Savings:** ${projection_data[year]['Savings']:,.2f}")
    st.markdown(f"- **📈 Investments:** ${projection_data[year]['Investments']:,.2f}")
    st.markdown(f"- **💳 Debt:** ${projection_data[year]['Debt']:,.2f}")
    st.markdown(f"- **📊 Net Worth:** ${projection_data[year]['Net Worth']:,.2f}")
    st.markdown(f"- **🏆 Credit Score:** {projection_data[year]['Credit Score']}")

st.markdown("---")
st.markdown("<h3>🔄 Come back anytime to track your progress!</h3>", unsafe_allow_html=True)
