import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="NSE 500 Dashboard", layout="wide")
st.title("📊 NSE 500 - Profit/Loss + Weekly Breadth Dashboard")

# Sidebar - View select
view = st.sidebar.selectbox("View Select Karo", ["1 Month","3 Month","6 Month","1 Year","5 Year"])
period_map = {"1 Month":"1mo","3 Month":"3mo","6 Month":"6mo","1 Year":"1y","5 Year":"5y"}
period = period_map[view]

symbols = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","ICICIBANK.NS","INFY.NS","SBIN.NS","BHARTIARTL.NS","ITC.NS","LT.NS","NTPC.NS","BHEL.NS","ONGC.NS","POWERGRID.NS","TATAPOWER.NS","ADANIENT.NS","ADANIGREEN.NS","IRFC.NS","MAZDOCK.NS","HAL.NS","BEL.NS"] # yaha 500 tak badha sakta hai

tab1, tab2 = st.tabs(["📈 Weekly Up/Down", "💰 Quarterly Profit/Loss"])

with tab1:
    st.subheader(f"Weekly Breadth - {view}")
    @st.cache_data(ttl=3600)
    def get_weekly_data(p):
        data = yf.download(symbols, period=p, interval="1wk", auto_adjust=True, progress=False, group_by='ticker', threads=True)
        try:
            closes = pd.DataFrame({s: data[s]['Close'] for s in symbols if s in data.columns.get_level_values(0)})
        except:
            closes = data['Close']
        weekly_change = closes.pct_change().dropna()
        up = (weekly_change > 0).sum(axis=1)
        down = (weekly_change < 0).sum(axis=1)
        return weekly_change.index, up, down

    dates, up, down = get_weekly_data(period)

    fig1 = go.Figure()
    fig1.add_bar(x=dates, y=up, name='UP', marker_color='#22c55e')
    fig1.add_bar(x=dates, y=down, name='DOWN', marker_color='#ef4444')
    fig1.update_layout(barmode='stack', height=450)
    st.plotly_chart(fig1, use_container_width=True)
    st.metric("Latest Week UP", int(up.iloc[-1]), f"{int(up.iloc[-1]-down.iloc[-1])} Net")

with tab2:
    st.subheader(f"Quarterly Profit/Loss - {view}")
    @st.cache_data(ttl=86400)
    def get_profit_data():
        rows=[]
        for sym in symbols[:20]:
            try:
                t=yf.Ticker(sym)
                q=t.quarterly_income_stmt
                if q is not None and 'Net Income' in q.index:
                    net=q.loc['Net Income']
                    for d,v in net.items():
                        rows.append({"Symbol":sym,"Quarter":pd.to_datetime(d),"Profit":v/1e7,"Type":"PROFIT" if v>0 else "LOSS"})
            except: pass
        return pd.DataFrame(rows)

    df = get_profit_data()
    if not df.empty:
        # Filter by view
        days = {"1 Month":90,"3 Month":180,"6 Month":365,"1 Year":365,"5 Year":1825}[view]
        df_f = df[df['Quarter'] >= pd.Timestamp.now() - pd.Timedelta(days=days)]

        profit_q = df_f[df_f['Type']=='PROFIT'].groupby('Quarter').size()
        loss_q = df_f[df_f['Type']=='LOSS'].groupby('Quarter').size()

        fig2 = go.Figure()
        fig2.add_bar(x=profit_q.index, y=profit_q.values, name='Profit Stocks', marker_color='#22c55e')
        fig2.add_bar(x=loss_q.index, y=loss_q.values, name='Loss Stocks', marker_color='#ef4444')
        fig2.update_layout(barmode='group', height=450)
        st.plotly_chart(fig2, use_container_width=True)
        st.dataframe(df_f.sort_values('Quarter', ascending=False).head(20))
    else:
        st.write("Data load ho raha hai, 1 min ruk...")

st.caption("Auto-update: Har ghante | Data: yfinance (NSE)")
