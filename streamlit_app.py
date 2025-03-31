import pandas as pd
import numpy as np
import streamlit as st
import locale

# Attempt to set locale to US English as a fallback
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    st.warning("Locale not supported. Using default settings.")

st.set_page_config(page_title="Finance Advisor", layout="centered")
st.markdown("""
    <style>
    body { background-color: #ffffff; color: #000000; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background-color: #000000; color: white; border-radius: 5px; }
    .stSlider .css-1cpxqw2 { color: #000000; }
    .stNumberInput input { color: #000000; }
    </style>
""", unsafe_allow_html=True)

class FinanceAdvisor:
    def __init__(self):
        self.income = 0
        self.expenses = 0
        self.savings = 0
        self.investments = 0
        self.federal_tax = 0.0
        self.state_tax = 0.0
        self.local_tax = 0.0
        self.credit_score = 0

    def collect_user_data(self):
        st.title("Finance Advisor")
        st.write("Welcome! Enter your financial information below to receive insights and personalized advice.")

        # Input with descriptions
        with st.expander("Income & Expenses Details"):
            self.income = st.number_input("Monthly Income (before taxes):", min_value=0.0)
            self.expenses = st.number_input("Monthly Expenses:", min_value=0.0)
            self.savings = st.number_input("Total Savings:", min_value=0.0)
            self.investments = st.number_input("Total Investments:", min_value=0.0)

        with st.expander("Tax Information"):
            self.federal_tax = st.slider("Federal Tax Rate (%)", 0, 50, 7) / 100
            self.state_tax = st.slider("State Tax Rate (%)", 0, 50, 15) / 100
            self.local_tax = st.slider("Local Tax Rate (%)", 0, 50, 20) / 100

        with st.expander("Credit Score and Additional Info"):
            self.credit_score = st.number_input("Credit Score (300-850):", min_value=300, max_value=850, value=700)

        if st.button("Generate Financial Report"):
            self.generate_financial_report()

    def safe_currency(self, value):
        try:
            return locale.currency(value, grouping=True)
        except ValueError:
            return f"${value:,.2f}"  # Fallback to basic USD format

    def generate_financial_report(self):
        total_tax_rate = self.federal_tax + self.state_tax + self.local_tax
        net_income = self.income * (1 - total_tax_rate)
        surplus = net_income - self.expenses
        net_worth = self.savings + self.investments

        st.subheader("Your Financial Report")
        st.write(f"**Gross Monthly Income:** {self.safe_currency(self.income)}")
        st.write(f"**Net Monthly Income After Taxes:** {self.safe_currency(net_income)}")
        st.write(f"**Monthly Expenses:** {self.safe_currency(self.expenses)}")
        st.write(f"**Total Savings:** {self.safe_currency(self.savings)}")
        st.write(f"**Total Investments:** {self.safe_currency(self.investments)}")
        st.write(f"**Credit Score:** {self.credit_score}")
        st.write(f"**Net Worth:** {self.safe_currency(net_worth)}")

        expense_to_income_ratio = (self.expenses / self.income) * 100 if self.income else 0
        savings_to_income_ratio = (self.savings / self.income) * 100 if self.income else 0
        investment_to_net_worth_ratio = (self.investments / net_worth) * 100 if net_worth else 0
        tax_burden = total_tax_rate * 100

        st.subheader("Additional Financial Statistics")
        st.write(f"**Expense to Income Ratio:** {expense_to_income_ratio:.2f}%")
        st.write(f"**Savings to Income Ratio:** {savings_to_income_ratio:.2f}%")
        st.write(f"**Investment to Net Worth Ratio:** {investment_to_net_worth_ratio:.2f}%")
        st.write(f"**Tax Burden:** {tax_burden:.2f}%")

        self.financial_health_grade(net_income, net_worth, surplus)
        st.write(self.generate_advice(surplus, net_worth))

    def generate_advice(self, surplus, net_worth):
        if surplus < 0:
            return "You are spending more than you earn. Consider reducing expenses or increasing your income."
        elif net_worth < 50000:
            return "Your net worth is growing, but consider increasing investments or reducing expenses."
        else:
            return "You are in excellent financial health. Continue your smart saving and investing strategies!"

    def financial_health_grade(self, net_income, net_worth, surplus):
        grade = 50.0
        if net_income >= 3000: grade += 20.0
        elif net_income >= 1500: grade += 10.0

        if net_worth >= 100000: grade += 20.0
        elif net_worth >= 50000: grade += 10.0

        if self.credit_score >= 750: grade += 10.0
        elif self.credit_score >= 650: grade += 5.0

        if surplus > 0: grade += 10.0
        elif surplus < 0: grade -= 10.0

        grade = max(0, min(grade, 100))
        st.subheader("Your Financial Health Grade")
        st.write(f"**Your Financial Health Grade:** {grade:.2f}/100")

if __name__ == "__main__":
    advisor = FinanceAdvisor()
    advisor.collect_user_data()
