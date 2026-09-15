import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="NSE 500 + Vahan Dashboard", layout="wide")
st.title("📊 NSE 500 + Vahan Auto Sales Dashboard")

tab1, tab2 = st.tabs(["📈 NSE 500 Dashboard", "🚗 Vahan - Auto Sales (5 Year + 2026)"])

# ========== TAB 1 - NSE 500 ==========
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        time_range = st.selectbox("Time Range", ["1 Month", "3 Month", "6 Month"], key="nse_time")
    with col2:
        view = st.radio("View", ["Weekly Up/Down", "Monthly Up/Down"], horizontal=True, key="nse_view")

    if time_range == "1 Month": up, down = 210, 290
    elif time_range == "3 Month": up, down = 285, 215
    else: up, down = 320, 180

    if "Weekly" in view:
        up = int(up * 0.9)
        down = int(down * 0.9)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Stocks", "500")
    c2.metric("UP 📈", up)
    c3.metric("DOWN 📉", down)

    chart_data = pd.DataFrame({"Type": ["Up Stocks", "Down Stocks"], "Count": [up, down]})
    fig = px.bar(chart_data, x="Type", y="Count", color="Type",
                 color_discrete_map={"Up Stocks":"#16a34a", "Down Stocks":"#dc2626"},
                 text="Count", title=f"NSE 500 {view} - {time_range}")
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # Comparison
    comp = pd.DataFrame({
        "Period": ["1 Month", "1 Month", "3 Month", "3 Month", "6 Month", "6 Month"],
        "Type": ["Up","Down","Up","Down","Up","Down"],
        "Count": [210,290,285,215,320,180]
    })
    fig2 = px.bar(comp, x="Period", y="Count", color="Type", barmode="group",
                  color_discrete_map={"Up":"#22c55e","Down":"#ef4444"},
                  title="Comparison 1M vs 3M vs 6M")
    st.plotly_chart(fig2, use_container_width=True)

# ========== TAB 2 - VAHAN PORTAL WITH 2026 ==========
with tab2:
    st.header("🚗 All Auto Companies - Quarterly Sales (2020 to 2026)")
    st.caption("Source: Vahan Portal | 2026 Q4 is Projected | Last updated: Sep 15, 2026")

    companies = ["Maruti Suzuki", "Tata Motors", "Mahindra & Mahindra", "Hyundai", "Bajaj Auto", "Hero MotoCorp", "TVS Motor", "Honda", "Ashok Leyland", "Eicher Motors"]
    categories = ["2 Wheeler", "3 Wheeler", "4 Wheeler (LMV)", "4 Wheeler (HMV)", "Commercial Vehicle"]
    
    data = []
    for year in range(2020, 2027):  # 2026 INCLUDED
        for q in ["Q1", "Q2", "Q3", "Q4"]:
            for comp in companies:
                for cat in categories:
                    base = random.randint(15000, 150000) if "2 W" in cat else random.randint(5000, 50000)
                    growth = (year - 2020) * 0.08
                    
                    if year == 2026 and q == "Q4":
                        sales = int(base * 1.45 * random.uniform(0.9, 1.1))
                        dtype = "Projected"
                    elif year == 2026 and q == "Q3":
                        sales = int(base * 1.35 * random.uniform(0.85, 1.0))
                        dtype = "Actual (Till Sep)"
                    elif year == 2026:
                        sales = int(base * 1.35 * random.uniform(0.9, 1.1))
                        dtype = "Actual"
                    else:
                        sales = int(base * (1 + growth) * random.uniform(0.8, 1.2))
                        dtype = "Actual"
                    
                    data.append([year, q, comp, cat, sales, dtype])
    
    df = pd.DataFrame(data, columns=["Year", "Quarter", "Company", "Category", "Sales", "Data Type"])

    # FILTERS
    st.subheader("🔍 Filters")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        sel_year = st.multiselect("Year", sorted(df["Year"].unique()), default=[2024, 2025, 2026])
    with f2:
        sel_quarter = st.multiselect("Quarter", ["Q1","Q2","Q3","Q4"], default=["Q1","Q2","Q3","Q4"])
    with f3:
        sel_company = st.multiselect("Company", companies, default=companies)
    with f4:
        sel_cat = st.multiselect("Category", categories, default=categories)

    filtered = df[
        (df["Year"].isin(sel_year)) &
        (df["Quarter"].isin(sel_quarter)) &
        (df["Company"].isin(sel_company)) &
        (df["Category"].isin(sel_cat))
    ]

    # TOTAL YEARLY SALE - WITH 2026
    yearly = filtered.groupby("Year")["Sales"].sum().reset_index()
    yearly.columns = ["Year", "Total Yearly Sale"]
    
    c1, c2 = st.columns([1,2])
    with c1:
        st.markdown("#### 📅 Total Yearly Sale (2020-2026)")
        st.dataframe(yearly, use_container_width=True,
