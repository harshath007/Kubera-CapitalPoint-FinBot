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
grade_color = "green" if score > 75 else "yellow" if score > 50 else "red"

# --- Financial Overview ---
st.subheader("📊 Your Financial Overview")
st.markdown(f"**💰 Net Monthly Income:** `${net_income:,.2f}`")
st.markdown(f"**📈 Net Worth:** `${net_worth:,.2f}`")
st.markdown(f"**💳 Debt-to-Income Ratio:** `{debt_to_income_ratio:.2f}%`")
st.markdown(f"**🚨 Emergency Fund:** `{emergency_fund:.2f}` months (Cap: 6 months)")
st.markdown(f"**💾 Emergency Fund Contribution:** `${savings_contribution:,.2f}`")

# --- Financial Score ---
st.markdown(f"<p class='score' style='color:{grade_color};'>💯 Financial Score: {score}/100</p>", unsafe_allow_html=True)

# --- Financial Distribution Chart ---
st.subheader("📊 Financial Distribution")
fig = go.Figure(data=[go.Pie(
    labels=["Savings", "Investments", "Debt"],
    values=[savings, investments, debt],
    hole=0.4
)])
fig.update_layout(showlegend=True, width=600, height=400)
st.plotly_chart(fig, use_container_width=True)

# --- National Comparison Report ---
st.subheader("📈 National Comparison Report")
national_avg_savings = 6000  
national_avg_income = 4500  
national_avg_debt = 30000  
national_avg_credit = 710  

comparison_report = f"""
- **Savings:** You have `{savings:,.2f}`. The U.S. average is `${national_avg_savings:,.2f}`.
- **Income:** Your income is `${income:,.2f}`. The U.S. median is `${national_avg_income:,.2f}`.
- **Debt:** Your debt is `${debt:,.2f}`. The U.S. average is `${national_avg_debt:,.2f}`.
- **Credit Score:** Your score is `{credit_score}`. The U.S. average is `{national_avg_credit}`.
"""
st.markdown(comparison_report)

# --- Financial Advice ---
st.subheader("📌 Personalized Financial Advice")
advice = []
if debt_to_income_ratio > 40:
    advice.append("⚠️ Your Debt-to-Income Ratio is **high!** Reduce debt.")
if savings_rate < 0.15:
    advice.append("📉 Increase your savings to at least **15%** of your income.")
if emergency_fund < 3:
    advice.append("🚨 Build up at least **3 months of savings** for emergencies.")
if investment_rate < 0.2:
    advice.append("📈 Increase your **investments** for long-term security.")
if credit_score < 600:
    advice.append("📉 Improve your **credit score** to access better financial options.")

if not advice:
    advice.append("✅ Your finances are in **great shape!** Keep up the good work!")

for tip in advice:
    st.markdown(f"- {tip}")

st.markdown("---")
st.markdown("<h3>🔁 Come back anytime to track your progress!</h3>", unsafe_allow_html=True)
