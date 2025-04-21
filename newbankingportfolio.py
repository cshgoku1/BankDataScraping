import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
from bankDataWebscraping import BankingWebdataScrapper
from BankingProductRecommender import BankingProductRecommender
import glob
import os

def load_latest_csv(data_type):
    files = glob.glob(f"scraped_data/{data_type}_*.csv")
    if not files:
        return pd.DataFrame()
    latest_file = max(files, key=os.path.getctime)
    return pd.read_csv(latest_file)

# Set page configuration
st.set_page_config(
    page_title="Banking Process Automation System",
    page_icon="🏦",
    layout="wide"
)

# Initialize session state by loading the latest scraped data
if 'savings_data' not in st.session_state:
    st.session_state.savings_data = load_latest_csv("savings")
if 'cd_data' not in st.session_state:
    st.session_state.cd_data = load_latest_csv("cd")
if 'checking_data' not in st.session_state:
    st.session_state.checking_data = load_latest_csv("checking")
if 'mm_data' not in st.session_state:
    st.session_state.mm_data = load_latest_csv("mm")

# Add sample customer data
if 'customers' not in st.session_state:
    # Create sample customer data
    st.session_state.customers = pd.DataFrame({
        'customer_id': range(1, 21),
        'name': [f"Customer {i}" for i in range(1, 21)],
        'age': np.random.randint(25, 65, 20),
        'income': np.random.randint(30000, 150000, 20),
        'credit_score': np.random.randint(580, 820, 20),
        'savings_balance': np.random.randint(1000, 100000, 20),
        'checking_balance': np.random.randint(500, 20000, 20),
        'mortgage_balance': [random.choice([0] + list(np.random.randint(50000, 500000, 1))) for _ in range(20)],
        'has_credit_card': [random.choice([True, False]) for _ in range(20)],
        'investment_balance': np.random.randint(0, 200000, 20),
        'last_activity': [(datetime.now() - timedelta(days=np.random.randint(1, 60))).strftime('%Y-%m-%d') for _ in range(20)]
    })

# App title and description
st.title("🏦 Banking Process Automation System")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("", [
    "Market Data Dashboard", 
    "Customer Portfolio Analysis"
])

# Scraper instance
scraper = BankingWebdataScrapper()

# Market Data Dashboard Page
if page == "Market Data Dashboard":
    st.header("📊 Banking Product Rates Dashboard")
    
    # Display data in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Savings", "💵 CD", "🪙 Checking", "📈 Money Market"])
    
    with tab1:
        st.subheader("Top Savings Accounts")
        if not st.session_state.savings_data.empty:
            # Add visualization of APY rates
            if 'APY' in st.session_state.savings_data.columns:
                # Extract numerical APY values 
                st.session_state.savings_data['APY_Value'] = st.session_state.savings_data['APY'].str.extract(r'(\d+\.\d+)').astype(float)
                
                # Sort by APY value
                sorted_data = st.session_state.savings_data.sort_values('APY_Value', ascending=False).head(10)
                
                # Horizontal bar chart
                fig = px.bar(
                    sorted_data,
                    y='BankName',
                    x='APY_Value',
                    orientation='h',
                    title='Top 10 Savings Account APY Rates',
                    labels={'APY_Value': 'APY (%)', 'BankName': 'Bank'}
                )
                st.plotly_chart(fig, use_container_width=True)

            # Display data table (excluding APY_Value)
            display_data = st.session_state.savings_data.drop(columns=['APY_Value'], errors='ignore')
            sorted_display_data = display_data.sort_values(by='BankName').reset_index(drop=True) 
            st.dataframe(sorted_display_data)
        else:
            st.info("No savings data available yet. Click 'Scrape All Data' to retrieve current rates.")

    
    with tab2:
        st.subheader("Top CD Accounts")
        if not st.session_state.cd_data.empty:
            if 'APY' in st.session_state.cd_data.columns:
                # Extract numerical APY values 
                st.session_state.cd_data['APY_Value'] = st.session_state.cd_data['APY'].str.extract(r'(\d+\.\d+)').astype(float)
                
                # Sort by APY value
                sorted_data = st.session_state.cd_data.sort_values('APY_Value', ascending=False).head(10)
                
                # Horizontal bar chart
                fig = px.bar(
                    sorted_data,
                    y='BankName',
                    x='APY_Value',
                    orientation='h',
                    title='Top 10 CD Account APY Rates',
                    labels={'APY_Value': 'APY (%)', 'BankName': 'Bank'}
                )
                st.plotly_chart(fig, use_container_width=True)

            # Display data table (excluding APY_Value)
            display_data = st.session_state.cd_data.drop(columns=['APY_Value'], errors='ignore')
            sorted_display_data = display_data.sort_values(by='BankName').reset_index(drop=True) 
            st.dataframe(sorted_display_data)

        else:
            st.info("No CD data available yet. Click 'Scrape All Data' to retrieve current rates.")
    
    with tab3:
        st.subheader("Top Checking Accounts")
        if not st.session_state.checking_data.empty:
            if 'APY' in st.session_state.checking_data.columns:
                st.session_state.checking_data['APY_Value'] = st.session_state.checking_data['APY'].str.extract(r'(\d+\.\d+)').astype(float)
                    
                    # Sort by APY value
                sorted_data = st.session_state.checking_data.sort_values('APY_Value', ascending=False).head(10)
                
                # Horizontal bar chart
                fig = px.bar(
                    sorted_data,
                    y='BankName',
                    x='APY_Value',
                    orientation='h',
                    title='Top 10 Checking Account APY Rates',
                    labels={'APY_Value': 'APY (%)', 'BankName': 'Bank'}
                )
                st.plotly_chart(fig, use_container_width=True)

            # Display data table (excluding APY_Value)
            display_data = st.session_state.checking_data.drop(columns=['APY_Value'], errors='ignore')
            sorted_display_data = display_data.sort_values(by='BankName').reset_index(drop=True) 
            st.dataframe(sorted_display_data)
        else:
            st.info("No checking account data available yet. Click 'Scrape All Data' to retrieve current rates.")
    
    with tab4:
        st.subheader("Top Money Market Accounts")
        if not st.session_state.mm_data.empty:
            if 'APY' in st.session_state.mm_data.columns:
                st.session_state.mm_data['APY_Value'] = st.session_state.mm_data['APY'].str.extract(r'(\d+\.\d+)').astype(float)
                    
                    # Sort by APY value
                sorted_data = st.session_state.mm_data.sort_values('APY_Value', ascending=False).head(10)
                
                # Horizontal bar chart
                fig = px.bar(
                    sorted_data,
                    y='BankName',
                    x='APY_Value',
                    orientation='h',
                    title='Top 10 Money Market Account APY Rates',
                    labels={'APY_Value': 'APY (%)', 'BankName': 'Bank'}
                )
                st.plotly_chart(fig, use_container_width=True)

            # Display data table (excluding APY_Value)
            display_data = st.session_state.mm_data.drop(columns=['APY_Value'], errors='ignore')
            sorted_display_data = display_data.sort_values(by='BankName').reset_index(drop=True) 
            st.dataframe(sorted_display_data)
        else:
            st.info("No money market data available yet. Click 'Scrape All Data' to retrieve current rates.")



elif page == "Customer Portfolio Analysis":
    st.title("🔍 Customer Portfolio Predictor")
    st.markdown("""
    Enter customer details below to get recommendations for the most suitable banking products.
    Our model analyzes financial attributes to suggest the best-fit options.
    """)

    # Initialize multi-output recommender
    recommender = BankingProductRecommender()

    st.header("🧾 Customer Features")
    with st.form("customer_input_form"):
        input_data = {
            'age': st.number_input("Age", min_value=18, max_value=100, value=30),
            'income': st.number_input("Annual Income ($)", min_value=10000, value=50000),
            'credit_score': st.number_input("Credit Score", min_value=300, max_value=850, value=700),
            'employment_status': st.selectbox("Employment Status", ["Employed", "Unemployed", "Self-employed", "Retired"]),
            'risk_tolerance': st.selectbox("Risk Tolerance", ["Low", "Medium", "High"]),
            'monthly_expense': st.number_input("Monthly Expense ($)", min_value=0, value=3000),
            'has_credit_card': st.checkbox("Has Credit Card", value=True),
            'investment_balance': st.number_input("Investment Balance ($)", min_value=0, value=5000)
        }

        submitted = st.form_submit_button("Predict Recommended Products")


    if submitted:
        with st.spinner("🔍 Predicting suitable banking products..."):
            try:
                predictions = recommender.recommend_all(input_data)

                label_map = {
                    "needs_savings_account": "Savings Account",
                    "needs_cd_account": "CD Account",
                    "needs_checking_account": "Checking Account",
                    "needs_money_market_account": "Money Market Account"
                }

                recommended_products = [label_map[key] for key, value in predictions.items() if value == 1]

                if recommended_products:
                    st.success("✅ Recommended Products:")
                    for product in recommended_products:
                        st.markdown(f"- **{product}**")
                else:
                    st.info("ℹ️ No strong product recommendation based on the current input.")

            except Exception as e:
                st.error("An error occurred during prediction:")


