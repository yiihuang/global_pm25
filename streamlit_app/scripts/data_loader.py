import pandas as pd
import streamlit as st
import os

# Using Streamlit's caching to speed up repeated data loading
@st.cache_data
def load_data():
    """
    This function loads the cleaned PM2.5 dataset from the data directory.
    It also extracts the 'Year' from the 'Period' column and adds it as a new column.

    Returns:
    - df: The cleaned DataFrame with an additional 'Year' column
    """
    try:
        # Try the local development path first
        filepath = "../data/processed/pm25_cleaned.csv"
        if not os.path.exists(filepath):
            # If not found, try the path relative to the script location
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = os.path.join(script_dir, "data", "pm25_cleaned.csv")
        
        # Load the data from the provided CSV file path
        df = pd.read_csv(filepath)
        
        # Convert the 'Period' column (which represents year in string format) to datetime and extract the year
        df['Year'] = pd.to_datetime(df['Period'], format='%Y').dt.year  # Only extract the year part
        
        # Return the dataframe with the new 'Year' column
        return df
    
    except FileNotFoundError:
        st.error("Data file not found. Please ensure pm25_cleaned.csv is in the correct location.")
        st.stop()
