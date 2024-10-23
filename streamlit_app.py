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
    fig = px.line(x=x_smooth_datetime, y=y_smooth, labels={'x': x_col, 'y': y_col}, t
