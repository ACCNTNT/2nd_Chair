import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.interpolate import make_interp_spline

# Function to load CSV files
def load_data(file):
    data = pd.read_csv(file)
    return data

# Function to create an interactive trendline graph
def plot_trendline(data, x_col, y_col):
    # Convert dates to datetime with error handling
    data[x_col] = pd.to_datetime(data[x_col], errors='coerce')  # Invalid dates become NaT
    data = data.dropna(subset=[x_col])  # Remove rows with invalid dates

    x = data[x_col]
    y = data[y_col]

    # Smooth the curve using spline interpolation
    x_smooth = np.linspace(x.min().timestamp(), x.max().timestamp(), 500)
    spl = make_interp_spline(x.map(pd.Timestamp.timestamp), y, k=3)  # Cubic spline
    y_smooth = spl(x_smooth)

    # Convert the smoothed x values back to datetime for plotting
    x_smooth_datetime = pd.to_datetime(x_smooth, unit='s')

    # Create the plot
    fig = px.line(x=x_smooth_datetime, y=y_smooth, labels={'x': x_col, 'y': y_col}, title=f'Trendline for {y_col} over {x_col}')
    fig.add_scatter(x=x, y=y, mode='markers', name='Data Points', marker=dict(color='blue'))
    
    # Update x-axis to show dates properly
    fig.update_layout(xaxis_title='Date')
    
    st.plotly_chart(fig)

# Function to visualize cash runway
def visualize_cash_runway(df):
    st.subheader("Cash Runway Visualization")
    
    # Create a new DataFrame for the runway visualization
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Invalid dates become NaT
    df = df.dropna(subset=['Date'])  # Remove rows with invalid dates

    runway_data = pd.DataFrame({
        'Date': df['Date'],
        'Cash Runway (Months)': df['Cash Runway (Months)']
    })
    
    # Create bar chart
    fig = px.bar(runway_data, x='Date', y='Cash Runway (Months)',
                 labels={'Date': 'Date', 'Cash Runway (Months)': 'Months of Cash Runway'},
                 title='Cash Runway Over Time')
    
    st.plotly_chart(fig)

# Function to compile and display assumptions
def display_assumptions(df):
    st.subheader("Assumptions")

    # Identify columns that contain 'Assumptions' or 'Assumption by Month'
    assumptions_columns = [col for col in df.columns if 'Assumptions' in col or 'Assumption' in col]

    if assumptions_columns:
        # Create a new DataFrame to show assumptions alongside the corresponding dates
        assumptions_data = df[['Date'] + assumptions_columns]
        assumptions_data.set_index('Date', inplace=True)
        
        # Display the assumptions DataFrame
        st.write(assumptions_data)
    else:
        st.write("No assumptions found in the uploaded file.")

# Streamlit app layout
st.title("ACCNTNT's Cash Forecast Visualization Tool")  # Updated title

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data from CSV
    df = load_data(uploaded_file)

    # Visualize cash runway first
    visualize_cash_runway(df)

    # Display assumptions
    display_assumptions(df)

    # Plot trendline for Closing Balance
    plot_trendline(df, 'Date', 'Closing Balance')

    # Display the dataframe preview
    st.write("Data Preview:")
    st.dataframe(df)

    # Check for necessary columns
    required_columns = ['Date', 'Closing Balance', 'Opening Balance', 'Monthly Cash Burn Rate', 'Cash Runway (Months)', 'Assumptions']
    if all(col in df.columns for col in required_columns):
        # Convert Date to datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Invalid dates become NaT
        df = df.dropna(subset=['Date'])  # Remove rows with invalid dates

        # Retrieve cash runway in months from the file
        cash_runway_months = df['Cash Runway (Months)'].iloc[0]

        # Display cash runway
        st.subheader("Cash Runway")
        st.write(f"Number of months of cash runway: {cash_runway_months:.2f} months")

        st.success("Cash flow forecast successfully generated!")
    else:
        st.error(f"CSV file must contain the following columns: {', '.join(required_columns)}.")
