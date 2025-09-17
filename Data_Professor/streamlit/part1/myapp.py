import yfinance as yf
import streamlit as st


# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'TSLA'

st.write(f"""
# Simple Stock Price App
Shown are the stock **closing price** and ***volume*** of {tickerSymbol}!
""")

st.subheader(tickerSymbol)

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(start='2018-09-01', end='2025-08-31')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.subheader('Closing Price')
st.line_chart(tickerDf.Close)

st.subheader('Volume')
st.line_chart(tickerDf.Volume)