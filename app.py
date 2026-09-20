import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

# NSE 500 ka Yahoo Finance par ticker symbol '^CRSLDX' hota hai
ticker_symbol = "^CRSLDX"

# Track karne ke liye alag-alag periods ki dictionary
periods = {
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "3 Years": "3y",
    "5 Years": "5y",
}

# Figure size set karein (3 rows aur 2 columns ka grid)
fig, axes = plt.subplots(3, 2, figsize=(15, 12))
axes = axes.flatten()

for i, (title, period) in enumerate(periods.items()):
  # Yahoo Finance se updated data download karein
  df = yf.download(ticker_symbol, period=period, interval="1d", progress=False)

  # Agar columns multi-index hain toh unhe flatten karein
  if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

  # Line chart plot karein
  axes[i].plot(df.index, df["Close"], color="#1f77b4", linewidth=1.5)
  axes[i].set_title(f"Nifty 500 Index - {title}", fontsize=12, fontweight="bold")
  axes[i].set_xlabel("Date", fontsize=10)
  axes[i].set_ylabel("Price", fontsize=10)
  axes[i].grid(True, linestyle="--", alpha=0.5)
  axes[i].tick_params(axis="x", rotation=30)

# Layout ko properly adjust karein
plt.tight_layout()

# Chart show karein
plt.show()
