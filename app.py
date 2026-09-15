import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NSE 500 Dashboard", layout="wide")
st.title("NSE 500 - Up / Down Dashboard")

# NSE 500 top symbols (sample 500 ke liye pura list use hota hai)
# Live ke liye yaha pura NSE 500 list lagega
symbols = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS"] # demo ke liye 5, code neeche 500 handle karega
# Actual 500 list ke liye:
# from nsepython import nsefetch - ya csv se

time_range = st.selectbox("Time Range Select Karo", ["1 Month", "3 Month", "6 Month"])
weekly_monthly = st.radio("View", ["Weekly", "Monthly"], horizontal=True)

period_map = {"1 Month":"1mo", "3 Month":"3mo", "6 Month":"6mo"}
interval_map = {"Weekly":"1wk", "Monthly":"1mo"}

if st.button("Data Load Karo"):
    up_count = 0
    down_count = 0
    results = []

    with st.spinner("NSE 500 data fetch ho raha hai..."):
        for sym in symbols:
            try:
                df = yf.download(sym, period=period_map[time_range], interval=interval_map[weekly_monthly], progress=False)
                if len(df) > 1:
                    change = (df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100
                    results.append({"Stock": sym, "Change %": round(float(change),2)})
                    if change > 0: up_count += 1
                    else: down_count += 1
            except: pass

    col1, col2 = st.columns(2)
    col1.metric("UP Stocks", up_count)
    col2.metric("DOWN Stocks", down_count)

    # Bar Chart
    chart_df = pd.DataFrame({"Type": ["Up", "Down"], "Count": [up_count, down_count]})
    fig = px.bar(chart_df, x="Type", y="Count", color="Type",
                 color_discrete_map={"Up":"#22c55e","Down":"#ef4444"},
                 title=f"NSE 500 {weekly_monthly} - {time_range} Up vs Down")
    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.dataframe(pd.DataFrame(results).sort_values("Change %", ascending=False), use_container_width=True)

# Pura NSE 500 ke liye - niche wala CSV use kar
st.markdown("---")
st.caption("Note: Demo me 5 stocks hain. Pura 500 chahiye to mujhe bol, main pura list wala code de dunga.")
