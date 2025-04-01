import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="KCP Finbot", page_icon="💰", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
        .main { background-color: #1a1a1a; color: #ffffff; }
        div.block-container { padding: 2rem; max-width: 900px; }
        .stButton>button { width: 100%; }
        h1, h2, h3 { text-align: center; color: #FFD700; }
        .score { font-size: 32px; text-align: center; font-weight: bold; }
        .section { border-bottom: 2px solid #FFD700; padding: 15px 0; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>💰 Kubera CapitalPoint Finbot</h1>", unsafe_allow_html=True)
st.markdown("<h3>Your Personal Financial Dashboard</h3>", unsafe_allow_html=True)

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

# --- Emergency Fund Calculation ---
emergency_fund = savings / (expenses * 6) if expenses > 0 else float('inf')

# --- Financial Score Calculation ---
score = 100

# Debt penalties
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

# Emergency Fund security
if emergency_fund < 3:
    score -= 10
elif emergency_fund < 6:
    score -= 5

# Credit Score impact
if credit_score < 600:
    score -= 15
elif credit_score < 700:
    score -= 5

# Age-based adjustments
if age < 30 and net_worth > 50000:
    score += 5  # Reward young savers
elif age > 50 and net_worth < 100000:
    score -= 10  # Penalize low net worth at later age

# Bonuses for strong financial habits
if debt == 0:
    score += 10
if savings_rate > 0.3:
    score += 5
if investment_rate > 0.25:
    score += 5
if credit_score > 750:
    score += 5

score = max(0, min(score, 100))  # Ensure score stays in 0-100 range
grade_color = "green" if score > 75 else "yellow" if score > 50 else "red"

# --- Financial Advice ---
def get_advice():
    advice = []
    if debt_to_income_ratio > 40:
        advice.append("⚠️ Your Debt-to-Income Ratio is **high!** Consider reducing debt.")
    if savings_rate < 0.15:
        advice.append("📉 Your savings rate is **below 15%**. Try to increase it.")
    if emergency_fund < 3:
        advice.append("🛑 You need at least 3 months of savings in your emergency fund.")
    if investment_rate < 0.2:
        advice.append("💡 Consider investing more for long-term financial security.")
    if credit_score < 600:
        advice.append("📉 Improve your **credit score** to access better financial options.")
    
    return advice if advice else ["✅ Your finances are in great shape! Keep it up!"]

advice = get_advice()

# --- Display Financial Overview ---
st.markdown("<div class='section'><h2>📊 Financial Overview</h2></div>", unsafe_allow_html=True)
st.markdown(f"**💰 Net Monthly Income:** `${net_income:,.2f}`")
st.markdown(f"**📈 Net Worth:** `${net_worth:,.2f}`")
st.markdown(f"**💳 Debt-to-Income Ratio:** `{debt_to_income_ratio:.2f}%`")
st.markdown(f"**🚨 Emergency Fund Coverage:** `{emergency_fund:.2f}` months (Goal: 6 months)")

# --- Financial Score ---
st.markdown(f"<p class='score' style='color:{grade_color};'>💯 Financial Score: {score}/100</p>", unsafe_allow_html=True)

# --- Personalized Advice ---
st.markdown("<div class='section'><h2>📌 Personalized Financial Advice</h2></div>", unsafe_allow_html=True)
for tip in advice:
    st.markdown(f"- {tip}")

# --- Financial Distribution Graph ---
st.markdown("<div class='section'><h2>📊 Financial Distribution</h2></div>", unsafe_allow_html=True)
fig = go.Figure(data=[go.Pie(
    labels=["Savings", "Investments", "Debt", "Assets"],
    values=[savings, investments, debt, assets],
    hole=0.4
)])
fig.update_layout(showlegend=True, width=600, height=400)
st.plotly_chart(fig, use_container_width=True)

# --- Conclusion ---
st.markdown("<h3>🔁 Track your progress regularly and make smart financial choices!</h3>", unsafe_allow_html=True)
