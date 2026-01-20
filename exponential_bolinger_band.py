import pandas as pd
import mplfinance as mpf
import yfinance as yf

start = '2024-01-01'
end = '2025-01-01'

btc = yf.Ticker('BTC-USD')
data = btc.history(start=start, end=end)

print(data)

def get_exponential_bollinger_bands(data, period):
    df = data.copy()
    df['ema'] = data.Close.ewm(span=period, adjust=False, min_periods=period).mean()
    df['upper'] = data.Close.ewm(span=period, adjust=False, min_periods=period).mean() + 2 * data.Close.ewm(span=period, adjust=False, min_periods=period).std()
    df['lower'] = data.Close.ewm(span=period, adjust=False, min_periods=period).mean() - 2 * data.Close.ewm(span=period, adjust=False, min_periods=period).std()

    return df

df = get_exponential_bollinger_bands(data, 20)
apd = mpf.make_addplot(df[['upper', 'ema', 'lower']])

mpf.plot(df, type='candle', style='yahoo', addplot=apd, title='BTC Exponential Bollinger Band', figsize=(11, 6))