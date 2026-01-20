import pandas as pd
import mplfinance as mpf
from binance.client import Client
import yfinance as yf

start = '2024-01-01'
end = '2025-01-01'

# data = yf.download('ETH-USD', period="id", start=start, end=end)

# print(data)
client = Client()

data = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1DAY, start, end)

# print(data)

ETH = pd.DataFrame(data, columns=['otime', 'open', 'high', 'low', 'close', 'volume', 'ctime', 'quote_vol',
                                  'no_trade', 'taker_base_volume', 'taker_quote_volume', 'ignore'])

ETH = ETH[['otime', 'open', 'high', 'low', 'close', 'volume']]
ETH['otime'] = pd.to_datetime(ETH['otime'], unit='ms')

ETH.set_index('otime', inplace=True)

ETH = ETH.astype(float)

print(ETH)

# mpf.plot(ETH.loc['2024-01':'2024-03'])

# mpf.plot(ETH.loc[:'2024-03'], type='candle')

# mpf.plot(ETH.loc['2024-07':], type='line')

# mpf.plot(ETH.loc['2024-06':'2024-12'], type='candle', volume=True, figsize=(20,10))

# mpf.plot(ETH.loc['2024-06':'2024-12'], hlines=dict(hlines=[2000,3500], colors=['r', 'g'], linestyle='--'), type='candle', volume=True, figsize=(20,10))

# mpf.plot(ETH.loc['2024-06':'2024-12'], hlines=dict(hlines=[2000,3500], colors=['r', 'g'], linestyle='-.'), type='candle', volume=True, figsize=(20,10))

# mpf.plot(ETH, type='candle', volume=True, mav=(12,26,50), title='ETH na ja', tight_layout=True, figratio=(8,4))

# make addplot

# ret = ETH['close'].pct_change(1) #daily
# ret = ETH['close'].pct_change(7) #weekly
ret = ETH['close'].pct_change(2) #2 days

print(ret)

# ret_add = mpf.make_addplot(ret, color='green', ylabel='return')
ret_add = mpf.make_addplot(ret, color='green', panel=2, ylabel='return')

# mpf.plot(ETH, addplot=ret_add, volume=True)

#mean of price 5 day
#calculate
print(ETH.close.rolling(5).mean())

#plot
ETH['EMA_5'] = ETH['close'].ewm(5, adjust=False, min_periods=5).mean()

emaplot = mpf.make_addplot(ETH['EMA_5'], color='green', ylabel='ema_5')

# mpf.plot(ETH, addplot=emaplot, style='charles')

# mpf.plot(ETH, style='charles')
mpf.plot(ETH[:'2024-05'], type='candle', style='yahoo', mav=(5,12,21), volume=True)