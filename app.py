import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Nifty 500 Market Dashboard", layout="wide")

st.title("📈 Nifty 500 Market Trend & Breadth Dashboard (3 Years)")
st.write("Yeh dashboard Nifty 500 index ka pichhle 3 saal ka trend aur market ki movement (Up/Down lines) ko darshata hai.")

# Nifty 500 Yahoo Finance Ticker Symbol
ticker_symbol = "^CRSLIST" # Nifty 500 index ticker on Yahoo Finance

@st.cache_data
def load_nifty500_data():
    # Fetching 3 years of daily/weekly data for Nifty 500
    df = yf.download("^CRSLIST", period="3y", interval="1wk")
    return df

with st.spinner("Nifty 500 ka 3 saal ka data load ho raha hai..."):
    data = load_nifty500_data()

if not data.empty:
    # Handling multi-index columns if returned by yfinance
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
        
    data = data.reset_index()
    
    # Calculate weekly price difference to check Up/Down movement
    data['Price_Change'] = data['Close'] - data['Open']
    data['Status'] = data['Price_Change'].apply(lambda x: 'Up' if x >= 0 else 'Down')
    data['Date'] = pd.to_datetime(data['Date']).dt.date

    # Creating a cumulative or rolling market movement line chart
    fig = go.Figure()

    # Line chart for Nifty 500 Closing Price trend
    fig.add_trace(go.Scatter(
        x=data['Date'], 
        y=data['Close'],
        mode='lines',
        name='Nifty 500 Close Price',
        line=dict(color='#3498db', width=2)
    ))

    fig.update_layout(
        title="Nifty 500 - 3 Year Weekly Price Trend Line Chart",
        xaxis_title="Hafte ki Taarikh",
        yaxis_title="Index Value",
        template="plotly_dark",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Market Breadth Representation (Simulated Up/Down count tracking based on momentum)
    st.subheader("📊 Market Breadth: Weekly Up vs Down Momentum")
    st.write("Pichhle 3 saalo me hafte-dar-hafte market ka rukh (Green vs Red weeks trend):")

    # Bar/Line combination for Up/Down status count
    up_weeks_count = len(data[data['Price_Change'] >= 0])
    down_weeks_count = len(data[data['Price_Change'] < 0])
    total_weeks = len(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Weeks Tracked", total_weeks)
    col2.metric("Market Up Weeks", up_weeks_count, delta=f"{round((up_weeks_count/total_weeks)*100, 1)}%")
    col3.metric("Market Down Weeks", down_weeks_count, delta=f"-{round((down_weeks_count/total_weeks)*100, 1)}%", delta_color="inverse")

    # Line chart showing cumulative Up/Down momentum over 3 years
    data['Cumulative_Trend'] = data['Price_Change'].cumsum()
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Cumulative_Trend'],
        mode='lines+markers',
        name='Cumulative Trend',
        line=dict(color='#2ecc71', width=2)
    ))
    fig2.update_layout(
        title="Cumulative Market Momentum Line Chart (3 Years)",
        xaxis_title="Date",
        yaxis_title="Cumulative Score",
        template="plotly_dark"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Raw data expander
    with st.expander("Nifty 500 ka Raw Data dekhein"):
        st.dataframe(data[['Date', 'Open', 'High', 'Low', 'Close', 'Price_Change', 'Status']])
else:
    st.error("Data load karne me error aayi. Kripya kuch der baad dobara koshish karein.")
