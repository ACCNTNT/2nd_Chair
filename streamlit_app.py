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
    # Convert dates to datetime
    x = pd.to_datetime(data[x_col])
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
    fig.update_layout(xaxis=dict(tickformat='%Y-%m'), xaxis_title=x_col)
    
    st.plotly_chart(fig)

# Streamlit app layout
st.title('Cash Flow Forecasting App')

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data from CSV
    df = load_data(uploaded_file)

    # Display the dataframe
    st.write("Data Preview:")
    st.dataframe(df)

    # Check for necessary columns
    required_columns = ['Date', 'Closing Balance']
    if all(col in df.columns for col in required_columns):
        # Convert Date to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Plot trendline for Closing Balance
        plot_trendline(df, 'Date', 'Closing Balance')

        st.success("Cash flow forecast successfully generated!")
    else:
        st.error(f"CSV file must contain the following columns: {', '.join(required_columns)}.")
