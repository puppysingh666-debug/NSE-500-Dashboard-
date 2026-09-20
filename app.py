import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import yfinance as yf

# 1. Page Configuration (Wide Layout)
st.set_page_config(
    page_title="Nifty 500 Multi-Period Dashboard", page_icon="📈", layout="wide"
)

st.title("📊 Nifty 500 Live Multi-Period Tracker")
st.markdown(
    "Yeh dashboard Yahoo Finance se live data fetch karke **1M, 3M, 6M, 1Y, 3Y, aur 5Y** ke line charts ek sath dikhata hai."
)
st.markdown("---")

# 2. Ticker aur Periods Setup
ticker_symbol = "^CRSLDX"
periods = {
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "3 Years": "3y",
    "5 Years": "5y",
}

# 3. Refresh Button
if st.button("🔄 Refresh Data"):
  st.rerun()

# 4. Loading State & Data Fetching
with st.spinner("Market data download ho raha hai... Kripya intezaar karein."):
  data_cache = {}
  for title, period in periods.items():
    df = yf.download(ticker_symbol, period=period, interval="1d", progress=False)
    # Multi-index fix for yfinance
    if isinstance(df.columns, pd.MultiIndex):
      df.columns = df.columns.get_level_values(0)
    data_cache[title] = df

# 5. Grid Layout me Charts Display Karna (2 Columns per row)
col1, col2 = st.columns(2)
col_list = [col1, col2]

i = 0
for title, period in periods.items():
  current_col = col_list[i % 2]

  with current_col:
    df = data_cache[title]

    if not df.empty:
      # Matplotlib figure
      fig, ax = plt.subplots(figsize=(8, 4))
      ax.plot(df.index, df["Close"], color="#007ACC", linewidth=1.5)
      ax.set_title(
          f"Nifty 500 - {title}", fontsize=11, fontweight="bold", color="#333333"
      )
      ax.set_xlabel("Date", fontsize=9)
      ax.set_ylabel("Price", fontsize=9)
      ax.grid(True, linestyle="--", alpha=0.5)
      plt.xticks(rotation=20)
      plt.tight_layout()

      # Streamlit me plot show karein
      st.pyplot(fig)

      # Latest Price aur Returns dikhana
      latest_price = float(df["Close"].iloc[-1])
      start_price = float(df["Close"].iloc[0])
      abs_change = latest_price - start_price
      pct_change = (abs_change / start_price) * 100

      color_tag = "normal" if pct_change >= 0 else "inverse"
      st.metric(
          label=f"Current Price ({title})",
          value=f"₹ {latest_price:,.2f}",
          delta=f"{pct_change:.2f}%",
      )
      st.markdown("---")
    else:
      st.warning(f"{title} ke liye data available nahi hai.")

  i += 1
