import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the Dashboard
st.title("📊 Interactive Monthly Data Analysis Dashboard")

# Upload Excel files
uploaded_files = st.file_uploader("Upload multiple Excel files", type=["xlsx"], accept_multiple_files=True)

data = []
if uploaded_files:
    for file in uploaded_files:
        df = pd.read_excel(file)
        df['Source'] = file.name  # Track file source
        data.append(df)
    df = pd.concat(data)
    
    # Convert 'Date' column to integer (day of the month)
    if 'Date' in df.columns:
        df['Date'] = pd.to_numeric(df['Date'], errors='coerce')  # Convert, setting errors to NaN
        df = df.dropna(subset=['Date'])  # Remove rows with NaN in 'Date'
        df['Date'] = df['Date'].astype(int)  # Now safely convert to int
    
    # Reshape data to long format
    df_melted = df.melt(id_vars=['Date'], var_name='Month', value_name='Value')
    
    # Sidebar filters
    st.sidebar.header("Filter Data")
    selected_month = st.sidebar.selectbox("Select Month", ['All'] + list(df_melted['Month'].unique()))
    
    # Filter data
    filtered_df = df_melted.copy()
    if selected_month != 'All':
        filtered_df = filtered_df[filtered_df['Month'] == selected_month]
    
    # Display filtered data
    st.write("### Filtered Data Preview")
    st.dataframe(filtered_df)
    
    # Visualization
    fig = px.line(filtered_df, x='Date', y='Value', color='Month', markers=True,
                  title='Daily Trends Over the Month', labels={'Date': 'Day of the Month', 'Value': 'Recorded Value'})
    st.plotly_chart(fig)
else:
    st.warning("Upload Excel files to proceed.")

# Run the app using: streamlit run script.py
