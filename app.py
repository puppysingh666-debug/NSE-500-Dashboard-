import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from io import BytesIO

st.set_page_config(layout="wide")
st.title("NSE 500 Dashboard - Working Version")

tab1, tab2 = st.tabs(["Weekly Breadth", "Companies Table"])

# TAB 1
with tab1:
    st.subheader("Last 3 Year Weekly Up vs Down")
    weeks = pd.date_range(end=datetime.now(), periods=156, freq='W')
    np.random.seed(42)
    up = np.random.randint(200, 400, 156)
    down = 500 - up
    net = up - down
    
    df_breadth = pd.DataFrame({
        "Week": weeks.strftime('%Y-%m-%d'),
        "Advances": up,
        "Declines": down,
        "Net": net
    })
    
    st.bar_chart(df_breadth.set_index("Week")["Net"])
    st.dataframe(df_breadth.tail(10))
    st.success(f"Latest Week: {up[-1]} Up / {down[-1]} Down")

# TAB 2
with tab2:
    st.subheader("Companies")
    data = {
        "Stock_Code": ["RELIANCE","TCS","KILITCH","SUNPHARMA","JSWSTEEL"],
        "Name": ["Reliance","TCS","Kilitch Drugs","Sun Pharma","JSW Steel"],
        "Sector": ["Energy","IT","Pharma","Pharma","Metals"],
        "Current_Price": [1420, 3850, 191, 1680, 950],
        "PE": [22, 28, 21, 32, 18],
        "Sector_PE": [24, 30, 35, 35, 20],
        "Debt_to_Equity": [0.4, 0.1, 0.32, 0.2, 1.1],
        "Pledge_%": [0, 0, 0, 0, 5.1],
        "Market_Cap_Cr": [1900000, 1400000, 661, 400000, 230000],
        "Capex_to_Revenue_Score": [0.8, 0.9, -0.1, 0.6, 0.3],
        "Screener_Link": ["https://www.screener.in/company/RELIANCE/"]*5
    }
    df_company = pd.DataFrame(data)
    st.dataframe(df_company, use_container_width=True)

# Download
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_breadth.to_excel(writer, sheet_name="Weekly_Breadth", index=False)
    df_company.to_excel(writer, sheet_name="Companies_Table", index=False)

st.download_button("📥 Download Excel (2 Tabs)", output.getvalue(), file_name="nse500_dashboard.xlsx")

st.caption("If this runs, we will add full 500 stocks in next step")
