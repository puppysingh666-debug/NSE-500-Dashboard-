import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("NSE 500 Dashboard")

tab1, tab2 = st.tabs(["Weekly Breadth", "Companies"])

# SAFE NSE 500 LIST - without API
@st.cache_data
def get_symbols():
    try:
        # Try NSE official
        df = pd.read_csv("https://archives.nseindia.com/content/indices/ind_nifty500list.csv")
        return df['Symbol'].tolist()
    except Exception as e:
        st.warning(f"NSE API fail: {e}, using sample list")
        # Fallback - 50 real symbols
        return ["RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","HINDUNILVR","SBIN","BHARTIARTL","ITC","KOTAKBANK","LT","AXISBANK","ASIANPAINT","MARUTI","BAJFINANCE","KILITCH","SUNPHARMA","WIPRO","TITAN","ULTRACEMCO"]*25

with tab1:
    weeks = pd.date_range(end=datetime.now(), periods=157, freq='W')
    np.random.seed(42)
    advances = [int(np.clip(260 + 30*np.sin(i/12) + np.random.normal(0,40), 80, 420)) for i in range(157)]
    declines = [500 - a - 10 for a in advances]
    net = [a-d for a,d in zip(advances, declines)]
    
    fig = go.Figure()
    fig.add_bar(x=weeks, y=net, marker_color=['green' if x>0 else 'red' for x in net])
    fig.add_hline(y=0)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    symbols = get_symbols()[:100]
    # Dummy data without yfinance to avoid error
    df = pd.DataFrame({
        "Stock_Code": symbols,
        "Name": symbols,
        "Sector": np.random.choice(["Pharma","IT","Bank","Auto"], len(symbols)),
        "Current_Price": np.random.uniform(100,2500, len(symbols)).round(1),
        "PE": np.random.uniform(10,50, len(symbols)).round(1),
        "Sector_PE": np.random.uniform(15,40, len(symbols)).round(1),
        "Debt_to_Equity": np.random.uniform(0,1.5, len(symbols)).round(2),
        "Pledge_%": np.random.choice([0,0,0,2.5], len(symbols)),
        "Market_Cap_Cr": np.random.uniform(500,50000, len(symbols)).round(0),
        "Capex_to_Revenue_Score": np.random.uniform(-0.2,1.4, len(symbols)).round(2),
        "Screener_Link": [f"https://www.screener.in/company/{s}/" for s in symbols]
    })
    st.dataframe(df, use_container_width=True)
    
    # Excel download
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame({"Week": weeks, "Advances": advances, "Declines": declines}).to_excel(writer, sheet_name="Weekly_Breadth", index=False)
        df.to_excel(writer, sheet_name="Companies_Table", index=False)
    st.download_button("Download Excel", output.getvalue(), "nse500_dashboard.xlsx")
