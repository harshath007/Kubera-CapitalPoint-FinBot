import pandas as pd
import numpy as np
import streamlit as st
import locale

locale.setlocale(locale.LC_ALL, '')
st.set_page_config(page_title="Finance Advisor", layout="centered")
st.markdown("""
    <style>
    body { background-color: #ffffff; color: #001f3f; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background-color: #001f3f; color: white; }
    .stSlider .css-1cpxqw2 { color: #001f3f; }
    .stNumberInput input { color: #001f3f; }
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
        st.title("🏦 Finance Advisor")
        st.write("Welcome! Enter your financial information below to receive insights and personalized advice.")

        # Input with descriptions
        with st.expander("Income & Expenses Details"):
            self.income = st.number_input("Enter your monthly income (before taxes):", min_value=0.0, help="This is your total gross income before any taxes or deductions.")
            self.expenses = st.number_input("Enter your monthly expenses:", min_value=0.0, help="Include all necessary expenses like rent, utilities, groceries, etc.")
            self.savings = st.number_input("Enter your total savings:", min_value=0.0, help="Include all funds saved in savings accounts, emergency funds, or cash reserves.")
            self.investments = st.number_input("Enter your total investments:", min_value=0.0, help="Include all investments in stocks, bonds, or other financial instruments.")

        with st.expander("Tax Information"):
            self.federal_tax = st.slider("Federal tax rate (%)", 0, 50, 7, help="Your federal tax rate is the percentage of your income taxed by the government.") / 100
            self.state_tax = st.slider("State tax rate (%)", 0, 50, 15, help="State taxes vary depending on your location.") / 100
            self.local_tax = st.slider("Local tax rate (%)", 0, 50, 20, help="Local taxes are usually imposed by cities or counties.") / 100

        with st.expander("Credit and Additional Info"):
            self.credit_score = st.number_input("Enter your credit score (300-850):", min_value=300, max_value=850, value=700, help="Your credit score impacts loan rates and financial opportunities.")

        if st.button("📊 Generate Financial Report"):
            self.generate_financial_report()

    def generate_financial_report(self):
        total_tax_rate = self.federal_tax + self.state_tax + self.local_tax
        net_income = self.income * (1 - total_tax_rate)
        surplus = net_income - self.expenses
        net_worth = self.savings + self.investments

        st.subheader("📈 Your Financial Report")
        st.write(f"**Gross Monthly Income:** {locale.currency(self.income, grouping=True)}")
        st.write(f"**Net Monthly Income After Taxes:** {locale.currency(net_income, grouping=True)}")
        st.write(f"**Monthly Expenses:** {locale.currency(self.expenses, grouping=True)}")
        st.write(f"**Total Savings:** {locale.currency(self.savings, grouping=True)}")
        st.write(f"**Total Investments:** {locale.currency(self.investments, grouping=True)}")
        st.write(f"**Credit Score:** {self.credit_score}")
        st.write(f"**Net Worth:** {locale.currency(net_worth, grouping=True)}")

        # Additional Statistics
        expense_to_income_ratio = (self.expenses / self.income) * 100 if self.income else 0
        savings_to_income_ratio = (self.savings / self.income) * 100 if self.income else 0
        investment_to_net_worth_ratio = (self.investments / net_worth) * 100 if net_worth else 0
        tax_burden = total_tax_rate * 100

        st.subheader("📊 Additional Financial Statistics")
        st.write(f"**Expense to Income Ratio:** {expense_to_income_ratio:.2f}%")
        st.write(f"**Savings to Income Ratio:** {savings_to_income_ratio:.2f}%")
        st.write(f"**Investment to Net Worth Ratio:** {investment_to_net_worth_ratio:.2f}%")
        st.write(f"**Tax Burden:** {tax_burden:.2f}%")

        self.financial_health_grade(net_income, net_worth, surplus)
        st.write(self.generate_advice(surplus, net_worth))

    def generate_advice(self, surplus, net_worth):
        if surplus < 0:
            return "⚠️ You are spending more than you earn. Consider reducing expenses or increasing your income."
        elif net_worth < 50000:
            return "💡 Your net worth is growing, but consider increasing investments or reducing expenses."
        else:
            return "🎉 You are in excellent financial health. Continue your smart saving and investing strategies!"

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
        st.subheader("🏁 Your Financial Health Grade")
        st.write(f"**Your Financial Health Grade:** {grade:.2f}/100")

if __name__ == "__main__":
    advisor = FinanceAdvisor()
    advisor.collect_user_data()
