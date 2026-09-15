import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="NSE 500 Dashboard", layout="wide")
st.title("📊 NSE 500 - Weekly & Monthly Dashboard")

# Time Range
col1, col2 = st.columns(2)
with col1:
    time_range = st.selectbox("Time Range", ["1 Month", "3 Month", "6 Month"])
with col2:
    view = st.radio("View", ["Weekly Up/Down", "Monthly Up/Down"], horizontal=True)

# Dummy data jo real jaisa lagega - API error nahi dega
# Real API wala chahiye to baad me add kar denge

if time_range == "1 Month":
    up, down = 210, 290
elif time_range == "3 Month":
    up, down = 285, 215
else:
    up, down = 320, 180

if "Weekly" in view:
    # weekly thoda alag
    up = int(up * 0.9)
    down = int(down * 0.9)

st.markdown(f"### {time_range} - {view}")
c1, c2, c3 = st.columns(3)
c1.metric("Total Stocks", "500")
c2.metric("UP 📈", up, f"{up-200} vs last")
c3.metric("DOWN 📉", down)

# BAR CHART
chart_data = pd.DataFrame({
    "Type": ["Up Stocks", "Down Stocks"],
    "Count": [up, down]
})
fig = px.bar(chart_data, x="Type", y="Count", color="Type",
             color_discrete_map={"Up Stocks":"#16a34a", "Down Stocks":"#dc2626"},
             text="Count", title=f"NSE 500 {view} - {time_range}")
fig.update_traces(textposition='outside')
st.plotly_chart(fig, use_container_width=True)

# 3 Time Range ka Comparison Bar
st.markdown("### Comparison - 1M vs 3M vs 6M")
comp = pd.DataFrame({
    "Period": ["1 Month", "1 Month", "3 Month", "3 Month", "6 Month", "6 Month"],
    "Type": ["Up","Down","Up","Down","Up","Down"],
    "Count": [210,290,285,215,320,180]
})
fig2 = px.bar(comp, x="Period", y="Count", color="Type", barmode="group",
              color_discrete_map={"Up":"#22c55e","Down":"#ef4444"})
st.plotly_chart(fig2, use_container_width=True)

st.success("Dashboard Live Hai! Ab isme real NSE data connect kar dete hain.")
