import pandas as pd
import mplfinance as mpf
import yfinance as yf

data = yf.download("BTC-USD", start="2018-01-01", end="2022-03-20")

print(data)

print(data.describe())

df = data['Close'].copy()

print(df)

# find average 1
print(data['Close'].mean())

# find average 2
print(data['Close'].describe())


#rolling = ข้อมูลจำนวณแท่งย้อนหลัง x แท่งจากแท่งปัจจุบัน

print(df.rolling(5).mean())

print(df.rolling(5).std())

sma_50 = df.rolling(50).mean()
sma_100 = df.rolling(100).mean()
sma_200 = df.rolling(200).mean()

print(sma_200)
# sma_200.plot()

# adjust=False จะตรงกับ trading view

ema_5 = df.ewm(span=5, adjust=False, min_periods=5).mean()
print(ema_5)

ema_10 = df.ewm(span=10, adjust=False, min_periods=10).mean()
print(ema_10)

ema_50 = df.ewm(span=50, adjust=False, min_periods=50).mean()
print(ema_50)

ema_50.plot()

data['ema_50'] = ema_50
data['sma_50'] = sma_50
data.plot(y=['Close','sma_50', 'ema_50'], figsize=(20,10))