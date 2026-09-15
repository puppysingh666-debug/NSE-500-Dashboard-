import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="NSE 500 Full Screener 2026", layout="wide")
st.title("💰 NSE 500 - Full 500 Companies Screener + Buy Logic")

# ================= REAL NSE 500 NAMES (Top 500) =================
# Real NSE 500 ke codes + company names (first 100 real, baaki auto-generated 400)
real_nse_500 = [
    "RELIANCE","TCS","HDFCBANK","ICICIBANK","INFY","BHARTIARTL","ITC","SBIN","LICI","LT",
    "HINDUNILVR","BAJFINANCE","MARUTI","SUNPHARMA","KOTAKBANK","ONGC","NTPC","AXISBANK","TITAN","ULTRACEMCO",
    "ADANIENT","ADANIPORTS","WIPRO","POWERGRID","JSWSTEEL","BAJAJFINSV","COALINDIA","HCLTECH","TATAMOTORS","ASIANPAINT",
    "M&M","BAJAJ-AUTO","SBILIFE","HDFCLIFE","DIVISLAB","GRASIM","BRITANNIA","TATASTEEL","EICHERMOT","DRREDDY",
    "CIPLA","TECHM","HINDALCO","HEROMOTOCO","UPL","BPCL","INDUSINDBK","ADANIGREEN","APOLLOHOSP","VEDL",
    "TATACONSUM","BAJAJHLDNG","PIDILITIND","SIEMENS","ADANIPOWER","SBICARD","TRENT","HAL","LTIM","DABUR",
    "BEL","IOC","ICICIPRULI","BANKBARODA","DLF","GAIL","INDIGO","PNB","AMBUJACEM","ICICIGI",
    "HAVELLS","GODREJCP","MARICO","SHRIRAMFIN","TATAPOWER","PFC","RECLTD","CHOLAFIN","BOSCHLTD","BERGEPAINT",
    "HDFCAMC","JINDALSTEL","INDIANB","ATGL","MUTHOOTFIN","NAUKRI","ADANIENSOL","ZOMATO","TVSMOTOR","TORNTPHARM",
    "MPHASIS","COLPAL","LUPIN","ABFRL","GODREJPROP","ASHOKLEY","SAIL","PERSISTENT","AUBANK","CONCOR"
]
# 400 aur companies generate karo - NSE 500 pura karne ke liye
while len(real_nse_500) < 500:
    real_nse_500.append(f"COMP{len(real_nse_500)+1}")

random.seed(42)
data = []
for i, code in enumerate(real_nse_500):
    close_price = random.randint(50, 15000)
    high_52w = int(close_price * random.uniform(1.05, 1.45))
    dma_200 = int(close_price * random.uniform(0.88, 1.12))
    market_cap = random.randint(2000, 800000)
    de = round(random.uniform(0.0, 1.8), 2)
    pledge = round(random.uniform(0, 25), 1)
    cum_avg = round(random.uniform(-5, 8), 1)
    trend = "Up" if random.random() > 0.4 else "Down"
    company_name = f"{code} Ltd" if i >= 100 else code # first 100 real names

    distance = round(((close_price - dma_200) / dma_200 * 100), 2)
    ma_from_high = round(((high_52w - close_price) / high_52w * 100), 2)

    # BUY Logic
    buy = "✅ BUY" if (abs(distance) <= 5 and trend == "Up" and cum_avg > 0 and pledge < 10) else "❌ Wait"

    data.append([code, company_name, close_price, market_cap, de, pledge, high_52w, dma_200, ma_from_high, cum_avg, trend, distance, buy])

df = pd.DataFrame(data, columns=[
    "NSE Code", "Company Name", "Close Price", "Market Cap (Cr)", "Debt to Equity",
    "Promoter Pledge %", "52 Week High", "200 DMA Price", "MA from 52W High %",
    "Cumulative Avg %", "10D Trend", "Distance from 200 DMA %", "BUY Signal"
])

# ================= FILTERS - HAR COLUMN ME FILTER =================
st.subheader("🔍 Har Column Me Filter")

f1, f2, f3, f4 = st.columns(4)
with f1:
    search_code = st.text_input("🔎 NSE Code Search (e.g. TATA)")
    search_company = st.text_input("🏢 Company Name Search")
with f2:
    close_min, close_max = st.slider("Close Price Range", 0, 15000, (0, 15000))
    mcap_min, mcap_max = st.slider("Market Cap (Cr) Range", 0, 800000, (0, 800000))
with f3:
    de_max = st.slider("Max Debt to Equity", 0.0, 2.0, 2.0)
    pledge_max = st.slider("Max Promoter Pledge %", 0.0, 25.0, 25.0)
with f4:
    dist_range = st.slider("Distance from 200 DMA % (-10 to +10)", -15.0, 15.0, (-15.0, 15.0))
    buy_filter = st.selectbox("BUY Signal", ["All", "Only ✅ BUY", "Only ❌ Wait"])
    trend_filter = st.selectbox("10D Trend", ["All", "Up", "Down"])

# Apply filters
filtered = df.copy()
if search_code:
    filtered = filtered[filtered["NSE Code"].str.contains(search_code.upper())]
if search_company:
    filtered = filtered[filtered["Company Name"].str.contains(search_company, case=False)]
filtered = filtered[(filtered["Close Price"] >= close_min) & (filtered["Close Price"] <= close_max)]
filtered = filtered[(filtered["Market Cap (Cr)"] >= mcap_min) & (filtered["Market Cap (Cr)"] <= mcap_max)]
filtered = filtered[filtered["Debt to Equity"] <= de_max]
filtered = filtered[filtered["Promoter Pledge %"] <= pledge_max]
filtered = filtered[(filtered["Distance from 200 DMA %"] >= dist_range[0]) & (filtered["Distance from 200 DMA %"] <= dist_range[1])]
if buy_filter!= "All":
    filtered = filtered[filtered["BUY Signal"] == buy_filter.replace("Only ", "")]
if trend_filter!= "All":
    filtered = filtered[filtered["10D Trend"] == trend_filter]

# ================= TABLE SHOW =================
st.markdown(f"### 📋 Showing {len(filtered)} / 500 Companies | BUY: {len(filtered[filtered['BUY Signal']=='✅ BUY'])}")

# Dataframe with built-in column filters (Streamlit new feature)
st.dataframe(
    filtered.style.apply(lambda x: ['background-color: #dcfce7' if v=="✅ BUY" else '' for v in x], subset=["BUY Signal"]),
    use_container_width=True,
    height=600,
    column
