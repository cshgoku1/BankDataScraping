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
    files = glob.glob(f"data/{data_type}_*.csv")
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
st.session_state.savings_data = load_latest_csv("savings")
st.session_state.cd_data = load_latest_csv("cd")
st.session_state.checking_data = load_latest_csv("checking")
st.session_state.mm_data = load_latest_csv("mm")


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

            # Display data table
            display_data = st.session_state.savings_data.drop(columns=['APY_Value'], errors='ignore')
            sorted_display_data = display_data.sort_values(by='BankName').reset_index(drop=True) 
            st.dataframe(sorted_display_data)
        else:
            st.info("No savings data available yet.")

    
    with tab2:
        st.subheader("Top CD Accounts")

        if not st.session_state.cd_data.empty :

            #get APY as numeric
            df = st.session_state.cd_data.copy()
            df['APY_Value'] = df['APY'].str.extract(r'(\d+\.\d+)').astype(float)

            # retain highest APY
            df = (df.sort_values('APY_Value', ascending=False).drop_duplicates(subset=['BankName'], keep='first').reset_index(drop=True))
            top10cdrates = df.head(10)

            #plot bar chart of those 10
            fig = px.bar(
                top10cdrates,
                y='BankName',
                x='APY_Value',
                orientation='h',
                title='Top 10 CD Account APY Rates',
                labels={'APY_Value': 'APY (%)', 'BankName': 'Bank'}
            )
            st.plotly_chart(fig, use_container_width=True)

            #display datatable
            display_data = (top10cdrates.drop(columns=['APY_Value']).sort_values('BankName').reset_index(drop=True))            
            st.dataframe(display_data)

        else:
            st.info("No CD data available yet.")
        
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

            # Display data table 
            display_data = st.session_state.checking_data.drop(columns=['APY_Value'], errors='ignore')
            sorted_display_data = display_data.sort_values(by='BankName').reset_index(drop=True) 
            st.dataframe(sorted_display_data)
        else:
            st.info("No checking account data available yet. ")
    
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

            # Display data table 
            display_data = st.session_state.mm_data.drop(columns=['APY_Value'], errors='ignore')
            sorted_display_data = display_data.sort_values(by='BankName').reset_index(drop=True) 
            st.dataframe(sorted_display_data)
        else:
            st.info("No money market data available yet.")



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
                    st.success("Recommended Products:")
                    for product in recommended_products:
                        st.markdown(f"- **{product}**")
                else:
                    st.info("No strong product recommendation based on the current input.")

            except Exception as e:
                st.error("An error occurred during prediction:")
