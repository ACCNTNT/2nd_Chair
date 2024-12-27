import streamlit as st
import pandas as pd
import numpy as np

# Function to load CSV files
def load_data(file):
    data = pd.read_csv(file)
    return data

# Function to calculate the metrics
def calculate_metrics(df):
    # Calculate Average Monthly Cash Burn
    df['Monthly Cash Burn'] = df['Opening Balance'] - df['Closing Balance']
    avg_cash_burn = df['Monthly Cash Burn'].mean()

    # Estimate the Zero Cash Date
    current_balance = df['Closing Balance'].iloc[0]
    months_to_zero = current_balance / avg_cash_burn if avg_cash_burn != 0 else 0
    zero_cash_date = pd.to_datetime(df['Date'].iloc[0]) + pd.DateOffset(months=months_to_zero)

    # Cash Burn Rate (Months)
    cash_burn_rate_months = current_balance / avg_cash_burn if avg_cash_burn != 0 else 0

    return avg_cash_burn, zero_cash_date, cash_burn_rate_months

# Streamlit app layout
st.title("Cash Burn | Year to Date")  # Updated title

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data from CSV
    df = load_data(uploaded_file)

    # Ensure that necessary columns are present before proceeding
    required_columns = ['Date', 'Closing Balance', 'Opening Balance']
    if all(col in df.columns for col in required_columns):
        # Convert Date to datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Invalid dates become NaT
        df = df.dropna(subset=['Date'])  # Remove rows with invalid dates

        # Calculate metrics
        avg_cash_burn, zero_cash_date, cash_burn_rate_months = calculate_metrics(df)

        # Display metrics in a similar layout as shown in the image
        st.subheader(f"Zero Cash Date (Assumption: No Additional Cash Inflows)")
        st.metric(label="Zero Cash Date", value=zero_cash_date.strftime('%m/%d/%Y'))

        st.subheader("Cash Burn Metrics")
        st.metric(label="Average Monthly Cash Burn", value=f"${avg_cash_burn:,.2f}")
        st.metric(label="Cash Burn Rate (Months)", value=f"{cash_burn_rate_months:.2f} Months")

        st.success("Cash flow forecast successfully generated!")

    else:
        st.error(f"CSV file must contain the following columns: {', '.join(required_columns)}.")
