import pandas as pd
import mplfinance as mpf
import yfinance as yf

start = '2024-01-01'
end = '2025-01-01'

btc = yf.Ticker('BTC-USD')
data = btc.history(start=start, end=end)

print(data)


def get_bollinger_bands(data, period):
    df = data.copy()
    df['sma'] = data.Close.rolling(period).mean()
    df['upper'] = data.Close.rolling(period).mean() + 2 * data.Close.rolling(period).std()
    df['lower'] = data.Close.rolling(period).mean() - 2 * data.Close.rolling(period).std()

    return df

df = get_bollinger_bands(data, 20)
apd = mpf.make_addplot(df[['upper', 'sma', 'lower']])

mpf.plot(df, type='candle', style='yahoo', addplot=apd, title='BTC Bollinger Band', figsize=(11,6))