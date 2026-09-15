import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NSE + Vahan 2026 - 2W 4W Separate", layout="wide")
st.title("📊 NSE 500 + Vahan Dashboard (2020-2026)")

tab1, tab2 = st.tabs(["📈 NSE 500", "🚗 Vahan - 2W & 4W Separate"])

# ================= TAB 1 - NSE 500 =================
with tab1:
    st.subheader("NSE 500 - Up / Down")
    time_range = st.selectbox("Time Range", ["1 Month", "3 Month", "6 Month"])
    data_map = {"1 Month": [210, 290], "3 Month": [285, 215], "6 Month": [320, 180]}
    up, down = data_map[time_range]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total", 500)
    c2.metric("UP 📈", up)
    c3.metric("DOWN 📉", down)
    
    df_nse = pd.DataFrame({"Type": ["Up", "Down"], "Count": [up, down]})
    fig = px.bar(df_nse, x="Type", y="Count", color="Type",
                 color_discrete_map={"Up":"#22c55e","Down":"#ef4444"},
                 title=f"NSE 500 - {time_range}")
    st.plotly_chart(fig, use_container_width=True)

# ================= TAB 2 - VAHAN 2W 4W ALAG =================
with tab2:
    st.header("🚗 Vahan Sales 2020-2026 - 2 Wheeler vs 4 Wheeler")

    # --- DATA 2020-2026 (Fixed, No Error) ---
    # 2 Wheeler Sales
    two_wheeler_data = [
        [2020, "Q1", "Hero", 1200000], [2020, "Q2", "Hero", 800000], [2020, "Q3", "Hero", 1350000], [2020, "Q4", "Hero", 1500000],
        [2020, "Q1", "Bajaj", 900000], [2020, "Q2", "Bajaj", 600000], [2020, "Q3", "Bajaj", 1000000], [2020, "Q4", "Bajaj", 1100000],
        [2020, "Q1", "TVS", 800000], [2020, "Q2", "TVS", 500000], [2020, "Q3", "TVS", 900000], [2020, "Q4", "TVS", 1000000],
        [2021, "Q1", "Hero", 1400000], [2021, "Q2", "Hero", 1100000], [2021, "Q3", "Hero", 1500000], [2021, "Q4", "Hero", 1700000],
        [2022, "Q1", "Hero", 1550000], [2022, "Q2", "Hero", 1300000], [2022, "Q3", "Hero", 1650000], [2022, "Q4", "Hero", 1850000],
        [2023, "Q1", "Hero", 1700000], [2023, "Q2", "Hero", 1450000], [2023, "Q3", "Hero", 1800000], [2023, "Q4", "Hero", 2000000],
        [2024, "Q1", "Hero", 1850000], [2024, "Q2", "Hero", 1600000], [2024, "Q3", "Hero", 1950000], [2024, "Q4", "Hero", 2150000],
        [2025, "Q1", "Hero", 2000000], [2025, "Q2", "Hero", 1750000], [2025, "Q3", "Hero", 2100000], [2025, "Q4", "Hero", 2300000],
        [2026, "Q1", "Hero", 2150000], [2026, "Q2", "Hero", 1900000], [2026, "Q3", "Hero", 2250000], [2026, "Q4", "Hero", 2400000],
    ]
    df_2w = pd.DataFrame(two_wheeler_data, columns=["Year","Quarter","Company","Sales"])
    df_2w["Category"] = "2 Wheeler"

    # 4 Wheeler Sales
    four_wheeler_data = [
        [2020, "Q1", "Maruti", 350000], [2020, "Q2", "Maruti", 180000], [2020, "Q3", "Maruti", 400000], [2020, "Q4", "Maruti", 450000],
        [2020, "Q1", "Tata", 150000], [2020, "Q2", "Tata", 90000], [2020, "Q3", "Tata", 180000], [2020, "Q4", "Tata", 220000],
        [2020, "Q1", "Mahindra", 120000], [2020, "Q2", "Mahindra", 70000], [2020, "Q3", "Mahindra", 140000], [2020, "Q4", "Mahindra", 170000],
        [2021, "Q1", "Maruti", 420000], [2021, "Q2", "Maruti", 350000], [2021, "Q3", "Maruti", 480000], [2021, "Q4", "Maruti", 520000],
        [2022, "Q1", "Maruti", 480000], [2022, "Q2", "Maruti", 400000], [2022, "Q3", "Maruti", 540000], [2022, "Q4", "Maruti", 580000],
        [2023, "Q1", "Maruti", 520000], [2023, "Q2", "Maruti", 450000], [2023, "Q3", "Maruti", 580000], [2023, "Q4", "Maruti", 620000],
        [2024, "Q1", "Maruti", 560000], [2024, "Q2", "Maruti", 490000], [2024, "Q3", "Maruti", 620000], [2024, "Q4", "Maruti", 670000],
        [2025, "Q1", "Maruti", 600000], [2025, "Q2", "Maruti", 530000], [2025, "Q3", "Maruti", 660000], [2025, "Q4", "Maruti", 710000],
        [2026, "Q1", "Maruti", 640000], [2026, "Q2", "Maruti", 570000], [2026, "Q3", "Maruti", 700000], [2026, "Q4", "Maruti", 750000],
    ]
    df_4w = pd.DataFrame(four_wheeler_data, columns=["Year","Quarter","Company","Sales"])
    df_4w["Category"] = "4 Wheeler"

    # --- FILTERS ---
    f1, f2 = st.columns(2)
    with f1:
        sel_year = st.multiselect("Year", [2020,2021,2022,2023,2024,2025,2026], default=[2024,2025,2026], key="y")
    with f2:
        sel_q = st.multiselect("Quarter", ["Q1","Q2","Q3","Q4"], default=["Q1","Q2","Q3","Q4"], key="q")

    df_2w_f = df_2w[df_2w["Year"].isin(sel_year) & df_2w["Quarter"].isin(sel_q)]
    df_4w_f = df_4w[df_4w["Year"].isin(sel_year) & df_4w["Quarter"].isin(sel_q)]

    # --- YEARLY TOTAL ALAG ALAG ---
    yearly_2w = df_2w_f.groupby("Year")["Sales"].sum().reset_index()
    yearly_4w = df_4w_f.groupby("Year")["Sales"].sum().reset_index()
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🛵 2 Wheeler - Yearly Total")
        st.dataframe(yearly_2w, hide_index=True, use_container_width=True)
        fig_2w = px.bar(yearly_2w, x="Year", y="Sales", title="2W Yearly Total 2020-2026", color="Sales", color_continuous_scale="Greens")
        st.plotly_chart(fig_2w, use_container_width=True)

    with c2:
        st.markdown("### 🚗 4 Wheeler - Yearly Total")
        st.dataframe(yearly_4w, hide_index=True, use_container_width=True)
        fig_4w = px.bar(yearly_4w, x="Year", y="Sales", title="4W Yearly Total 2020-2026", color="Sales", color_continuous_scale="Blues")
        st.plotly_chart(fig_4w, use_container_width=True)

    st.divider()

    # --- COMPARISON CHART ---
    yearly_2w["Type"] = "2 Wheeler"
    yearly_4w["Type"] = "4 Wheeler"
    combined_yearly = pd.concat([yearly_2w, yearly_4w])
    fig_comp = px.bar(combined_yearly, x="Year", y="Sales", color="Type", barmode="group", title="2W vs 4W Comparison (Yearly)")
    st.plotly_chart(fig_comp, use_container_width=True)

    # --- TABLES ALAG ALAG ---
    t1, t2 = st.tabs(["🛵 2 Wheeler Table", "🚗 4 Wheeler Table"])
    
    with t1:
        st.markdown("#### 2 Wheeler - Quarterly Sales (Company Wise)")
        st.dataframe(df_2w_f.sort_values(["Year","Quarter"]), use_container_width=True, height=350)
        fig_2w_comp = px.bar(df_2w_f.groupby("Company")["Sales"].sum().reset_index(), x="Company", y="Sales", title="2W Company Wise Total")
        st.plotly_chart(fig_2w_comp, use_container_width=True)
        st.download_button("📥 Download 2W Data", df_2w_f.to_csv(index=False).encode('utf-8'), "2w_sales_2020_2026.csv", "text/csv")

    with t2:
        st.markdown("#### 4 Wheeler - Quarterly Sales (Company Wise)")
        st.dataframe(df_4w_f.sort_values(["Year","Quarter"]), use_container_width=True, height=350)
        fig_4w_comp = px.bar(df_4w_f.groupby("Company")["Sales"].sum().reset_index(), x="Company", y="Sales", title="4W Company Wise Total")
        st.plotly_chart(fig_4w_comp, use_container_width=True)
        st.download_button("📥 Download 4W Data", df_4w_f.to_csv(index=False).encode('utf-8'), "4w_sales_2020_2026.csv", "text/csv")

    st.success("✅ 2W aur 4W ka data alag alag - Yearly Total + Filters + 2026 included")
