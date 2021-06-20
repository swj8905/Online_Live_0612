import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import datetime

ticker = st.text_input("티커 입력")
data = yf.Ticker(ticker)
df = data.history(period='1d', start='2015-1-1',
             end=datetime.datetime.today().strftime("%Y-%m-%d"))

st.write("## 주가 - 종가 기준")
st.line_chart(df["Close"])

st.write("## 주가 - 캔들 차트")
layout = go.Layout(yaxis = {"fixedrange":False})
candle = go.Candlestick(x=df.index, open=df["Open"], high=df["High"],
                        low=df["Low"], close=df["Close"])
fig = go.Figure(data=candle, layout=layout)
st.plotly_chart(fig)

st.write("## 거래량")
st.bar_chart(df["Volume"])
