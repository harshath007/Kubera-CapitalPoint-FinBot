import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="KCP Finbot", page_icon="💰", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
        .main { background-color: #1a1a1a; color: #ffffff; }
        div.block-container { padding: 2rem; max-width: 1200px; }
        .stButton>button { width: 100%; }
        h1, h2, h3, p, div, span, li, ul, ol { color: #ffffff !important; }
        .score { font-size: 32px; text-align: center; font-weight: bold; }
        .section { border-bottom: 2px solid #FFD700; padding: 15px 0; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>💰 Kubera CapitalPoint Finbot</h1>", unsafe_allow_html=True)
st.markdown("<h3>Your Personal Financial Dashboard & Predictions</h3>", unsafe_allow_html=True)

# --- Sidebar (User Inputs) ---
st.sidebar.header("📊 User Input")
income = st.sidebar.number_input("💵 Monthly Income (Before Taxes): $", min_value=0.0, format="%.2f")
expenses = st.sidebar.number_input("💸 Monthly Expenses (Including Taxes): $", min_value=0.0, format="%.2f")
savings = st.sidebar.number_input("🏦 Total Savings: $", min_value=0.0, format="%.2f")
investments = st.sidebar.number_input("📈 Total Investments: $", min_value=0.0, format="%.2f")
debt = st.sidebar.number_input("💳 Current Debt: $", min_value=0.0, format="%.2f")
assets = st.sidebar.number_input("🏡 Total Asset Value: $", min_value=0.0, format="%.2f")
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
emergency_fund = savings / (expenses * 6) if expenses > 0 else float('inf')

# --- National Averages (U.S. Data for Comparison) ---
us_avg_net_worth = 120000
us_avg_savings = 7000
us_avg_income = 65000
us_avg_debt = 30000

# --- National Standing Analysis ---
def get_national_standing():
    standing = []
    if net_worth > us_avg_net_worth:
        standing.append("🌟 You have **above-average net worth!**")
    else:
        standing.append("⚠️ Your **net worth is below** the national average.")

    if savings > us_avg_savings:
        standing.append("💰 Your **savings exceed** the national median.")
    else:
        standing.append("📉 You should **increase your savings** to match the national level.")

    if income > us_avg_income:
        standing.append("📈 Your **income is higher** than the national average!")
    else:
        standing.append("💵 Your **income is below** the national average.")

    if debt < us_avg_debt:
        standing.append("✅ You have **less debt** than the national average.")
    else:
        standing.append("⚠️ Your **debt level is higher** than the U.S. median.")

    return standing

national_standing = get_national_standing()

# --- Financial Score Calculation ---
score = 100

# Debt impact
if debt_to_income_ratio > 40:
    score -= 20
elif debt_to_income_ratio > 30:
    score -= 15
elif debt_to_income_ratio > 20:
    score -= 10

# Savings & Investment impact
if savings_rate < 0.15:
    score -= 10
if investment_rate < 0.2:
    score -= 10

# Emergency Fund
if emergency_fund < 3:
    score -= 10
elif emergency_fund < 6:
    score -= 5

# Age-based adjustments
if age < 30 and net_worth > 50000:
    score += 5
elif age > 50 and net_worth < 100000:
    score -= 10

# Credit Score impact
if credit_score < 600:
    score -= 15
elif credit_score < 700:
    score -= 5

# Bonuses for strong financial habits
if debt == 0:
    score += 10
if savings_rate > 0.3:
    score += 5
if investment_rate > 0.25:
    score += 5
if credit_score > 750:
    score += 5

score = max(0, min(score, 100))
grade_color = "green" if score > 75 else "yellow" if score > 50 else "red"

# --- Financial Predictions ---
def forecast_years(years):
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

projection_years = [2, 5, 10]
projection_data = {year: forecast_years(year) for year in projection_years}

# --- Display Sections ---
st.markdown("<h2>📌 National Standing</h2>", unsafe_allow_html=True)
for fact in national_standing:
    st.markdown(f"- {fact}")

st.markdown(f"<p class='score' style='color:{grade_color};'>💯 Financial Score: {score}/100</p>", unsafe_allow_html=True)

st.markdown("<h2>🚀 Financial Projections</h2>", unsafe_allow_html=True)
for year in projection_years:
    st.markdown(f"### In {year} years:")
    st.markdown(f"💰 Income: **${projection_data[year]['Income']:,.2f}**")
    st.markdown(f"🏦 Savings: **${projection_data[year]['Savings']:,.2f}**")
    st.markdown(f"📈 Investments: **${projection_data[year]['Investments']:,.2f}**")

st.markdown("<h3>🔁 Stay on top of your finances!</h3>", unsafe_allow_html=True)
