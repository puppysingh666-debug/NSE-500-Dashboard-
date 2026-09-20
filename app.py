import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Nifty 50 Weekly Dashboard", layout="wide")

st.title("📈 Nifty 50 Stocks Weekly Up/Down Dashboard (3 Years)")
st.write("Yeh dashboard pichhle 3 saal ka weekly price movement (Open vs Close) bar chart ke roop me dikhata hai.")

# Popular Nifty 50 stocks dictionary (Yahoo Finance symbols ke sath)
nifty_stocks = {
    "Reliance Industries": "RELIANCE.NS",
    "TCS (Tata Consultancy Services)": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "State Bank of India (SBI)": "SBIN.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "ITC Limited": "ITC.NS",
    "Larsen & Toubro (L&T)": "LT.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS"
}

# Dropdown menu to select stock
selected_name = st.selectbox("Koi stock chunen:", list(nifty_stocks.keys()))
ticker = nifty_stocks[selected_name]

# Function to load data with caching for speed
@st.cache_data
def load_data(ticker_symbol):
    # Fetching 3 years of weekly data
    df = yf.download(ticker_symbol, period="3y", interval="1wk")
    return df

with st.spinner(f"Fetching data for {selected_name}..."):
    data = load_data(ticker)

if not data.empty:
    # Handling multi-index columns if returned by yfinance
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
        
    data = data.reset_index()
    
    # Calculate weekly change (Close - Open)
    data['Weekly_Change'] = data['Close'] - data['Open']
    data['Color'] = data['Weekly_Change'].apply(lambda x: 'Green (Up)' if x >= 0 else 'Red (Down)')
    data['Date'] = pd.to_datetime(data['Date']).dt.date

    # Plotting interactive bar chart using Plotly
    fig = px.bar(
        data, 
        x='Date', 
        y='Weekly_Change', 
        color='Color',
        color_discrete_map={'Green (Up)': '#2ecc71', 'Red (Down)': '#e74c3c'},
        title=f"{selected_name} - Weekly Up/Down Analysis (Last 3 Years)",
        labels={'Weekly_Change': 'Price Change (Close - Open in INR)', 'Date': 'Week Starting'}
    )
    
    fig.update_layout(
        xaxis_title="Hafte ki Taarikh",
        yaxis_title="Price Difference (₹)",
        template="plotly_dark"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary Metrics
    total_weeks = len(data)
    up_weeks = len(data[data['Weekly_Change'] >= 0])
    down_weeks = len(data[data['Weekly_Change'] < 0])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Hafte (3 Years)", total_weeks)
    col2.metric("Green Weeks (Up)", up_weeks, delta=f"{round((up_weeks/total_weeks)*100, 1)}%")
    col3.metric("Red Weeks (Down)", down_weeks, delta=f"-{round((down_weeks/total_weeks)*100, 1)}%", delta_color="inverse")
    
    # Show Raw Data Expander
    with st.expander("Aakhri hafte ka Raw Data dekhein"):
        st.write(data[['Date', 'Open', 'High', 'Low', 'Close', 'Weekly_Change']].tail(15))
else:
    st.error("Data load karne me samasya aayi. Kripya dobara koshish karein.")
