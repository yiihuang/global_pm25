# ====================== Import Required Libraries ======================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scripts.data_loader import load_data
from scripts.visualizations import create_violin_plot

# ======================== Streamlit Page Setup ========================
st.set_page_config(page_title="Residence Area Analysis", layout="wide")
st.title("🏘️ PM2.5 Analysis by Residence Area Type")

# ========================= Load Data ==========================
df = load_data()

# ========================= Sidebar Filters ==========================
st.sidebar.header("Filters")

# Year slider for selecting a specific year
selected_year = st.sidebar.slider(
    "Select Year",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=int(df['Year'].max())
)

# ========================= Main Content ==========================
st.header("PM2.5 Distribution by Residence Area Type")

# Create violin plot for PM2.5 distribution by residence area type
st.plotly_chart(create_violin_plot(df), use_container_width=True)

# Create tabs for different analyses
tab1, tab2, tab3 = st.tabs(["Global Trends", "Cleanest Countries", "Most Polluted Countries"])

# Tab 1: Global Trends
with tab1:
    st.subheader("Global PM2.5 Trends by Residence Area Type")
    
    # Group by Dim1 and Period, calculate mean PM2.5 values
    dim1_period_summary = df.groupby(['Dim1', 'Period'])['FactValueNumeric'].mean().reset_index()
    
    # Create line plot using plotly
    fig = px.line(dim1_period_summary, 
                  x='Period', 
                  y='FactValueNumeric', 
                  color='Dim1',
                  markers=True,
                  title='Mean PM2.5 Values by Residence Area Type Over Time')
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='PM2.5 Values (µg/m³)',
        legend_title='Residence Area Type',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Cleanest Countries
with tab2:
    st.subheader("PM2.5 Trends in Top 10 Cleanest Countries")
    
    # Identify top 10 cleanest countries
    cleanest_countries = df.groupby('Location')['FactValueNumeric'].mean().sort_values().head(10)
    
    # Filter data for these countries
    clean_countries_df = df[df['Location'].isin(cleanest_countries.index)]
    
    # Group by Dim1 and Period
    clean_summary = clean_countries_df.groupby(['Dim1', 'Period'])['FactValueNumeric'].mean().reset_index()
    
    # Create line plot
    fig = px.line(clean_summary, 
                  x='Period', 
                  y='FactValueNumeric', 
                  color='Dim1',
                  markers=True,
                  title='Mean PM2.5 Values by Residence Area Type Over Time\n(Top 10 Cleanest Countries)')
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='PM2.5 Values (µg/m³)',
        legend_title='Residence Area Type',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display list of cleanest countries with their mean PM2.5 values
    st.write("Top 10 Cleanest Countries:")
    cleanest_df = pd.DataFrame({
        'Country': cleanest_countries.index,
        'Mean PM2.5 (µg/m³)': cleanest_countries.values.round(2)
    })
    st.dataframe(cleanest_df, hide_index=True)

# Tab 3: Most Polluted Countries
with tab3:
    st.subheader("PM2.5 Trends in Top 10 Most Polluted Countries")
    
    # Identify top 10 most polluted countries
    polluted_countries = df.groupby('Location')['FactValueNumeric'].mean().sort_values(ascending=False).head(10)
    
    # Filter data for these countries
    polluted_countries_df = df[df['Location'].isin(polluted_countries.index)]
    
    # Group by Dim1 and Period
    polluted_summary = polluted_countries_df.groupby(['Dim1', 'Period'])['FactValueNumeric'].mean().reset_index()
    
    # Create line plot
    fig = px.line(polluted_summary, 
                  x='Period', 
                  y='FactValueNumeric', 
                  color='Dim1',
                  markers=True,
                  title='Mean PM2.5 Values by Residence Area Type Over Time\n(Top 10 Most Polluted Countries)')
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='PM2.5 Values (µg/m³)',
        legend_title='Residence Area Type',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display list of most polluted countries with their mean PM2.5 values
    st.write("Top 10 Most Polluted Countries:")
    polluted_df = pd.DataFrame({
        'Country': polluted_countries.index,
        'Mean PM2.5 (µg/m³)': polluted_countries.values.round(2)
    })
    st.dataframe(polluted_df, hide_index=True)

# ========================= Sidebar About Section ==========================
st.sidebar.header("About")
st.sidebar.info("""
This page analyzes PM2.5 levels across different residence area types (Cities, Rural, Total).
The analysis includes:
- Global trends over time
- Trends in the 10 cleanest countries
- Trends in the 10 most polluted countries
""") 