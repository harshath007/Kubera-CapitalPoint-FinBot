import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="KCP Finbot", page_icon="💰", layout="wide")

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
st.markdown("<h1>💰 Kubera CapitalPoint Finbot</h1>", unsafe_allow_html=True)
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
emergency_fund_cap = 6  # Max 6 months of expenses
emergency_fund = min(savings / (expenses / 12), emergency_fund_cap) if expenses > 0 else float('inf')

# Only allocate a portion of savings if not at the cap
needed_savings_for_fund = max(0, (expenses / 12) * emergency_fund_cap - savings)
if needed_savings_for_fund > 0:
    savings_contribution = min(needed_savings_for_fund * 0.3, savings)  # 30% of needed amount
else:
    savings_contribution = 0

# --- National Percentile Report (Based on Age) ---
# (Fake percentiles for now, replace with real data later)
income_percentile = np.interp(income, [20000, 100000, 250000], [30, 70, 95])
savings_percentile = np.interp(savings, [5000, 50000, 200000], [25, 60, 90])
investment_percentile = np.interp(investments, [1000, 50000, 150000], [20, 65, 85])
debt_percentile = np.interp(debt, [0, 20000, 100000], [90, 50, 20])  # Inverse scale (low debt = high score)
credit_percentile = np.interp(credit_score, [500, 700, 800], [20, 60, 90])

# --- Financial Grading System (0-100) ---
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

# Bonuses for good financial habits
if credit_score > 750:
    score += 5
if debt == 0:
    score += 10
if savings_rate > 0.3:
    score += 5
if investment_rate > 0.25:
    score += 5

score = max(0, min(score, 100))  # Ensure score stays in 0-100 range
grade_color = "green" if score > 75 else "yellow" if score > 50 else "red"

# --- Display Financial Overview ---
st.subheader("📊 Your Financial Overview")
st.markdown(f"**💰 Net Monthly Income:** `${net_income:,.2f}`")
st.markdown(f"**📈 Net Worth:** `${net_worth:,.2f}`")
st.markdown(f"**💳 Debt-to-Income Ratio:** `{debt_to_income_ratio:.2f}%`")
st.markdown(f"**🚨 Emergency Fund:** `{emergency_fund:.2f}` months (Cap: 6 months)")
st.markdown(f"**💾 Emergency Fund Contribution:** `${savings_contribution:,.2f}`")

# --- Financial Score ---
st.markdown(f"<p class='score' style='color:{grade_color};'>💯 Financial Score: {score}/100</p>", unsafe_allow_html=True)

# --- National Standing Report ---
st.subheader("📌 National Standing Report (Lower is Better)")
st.markdown(f"- **Income Percentile:** {income_percentile:.0f}th")
st.markdown(f"- **Savings Percentile:** {savings_percentile:.0f}th")
st.markdown(f"- **Investments Percentile:** {investment_percentile:.0f}th")
st.markdown(f"- **Debt Percentile:** {debt_percentile:.0f}th")
st.markdown(f"- **Credit Score Percentile:** {credit_percentile:.0f}th")

# --- Data Visualization ---
st.subheader("📊 Financial Distribution")
fig = go.Figure(data=[go.Pie(
    labels=["Savings", "Investments", "Debt"],
    values=[savings, investments, debt],
    hole=0.4
)])
fig.update_layout(showlegend=True, width=600, height=400)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("<h3>🔁 Come back anytime to track your progress!</h3>", unsafe_allow_html=True)
