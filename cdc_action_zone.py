import pandas as pd
import mplfinance as mpf
from binance.client import Client
import matplotlib.pyplot as plt

client = Client()

bars = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1DAY, '1 Jan, 2021', '1 Jan, 2022')
df = pd.DataFrame(bars, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume',
                                 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume',
                                 'Ignore'])
df = df.apply(pd.to_numeric)
df['Date'] = pd.to_datetime(df['Date'], unit='ms')
df.set_index('Date', inplace=True)
df = df.iloc[:, :5]

print(df)

# mpf.plot(df)

df['ema_short'] = df.Close.ewm(span=12, adjust=False, min_periods=12).mean()
df['ema_long'] = df.Close.ewm(span=26, adjust=False, min_periods=26).mean()

ema_short = mpf.make_addplot(df.ema_short, color='orange')
ema_long = mpf.make_addplot(df.ema_long, color='y')

# mpf.plot(df, style='yahoo', type='candle', addplot=[ema_short, ema_long], figsize=(14, 6))

print(df)

df['trend'] = df['ema_short'] > df['ema_long']

print(df[df['trend'] == True])

df['trend_shift'] = df.trend.shift(1)

print(df)

print(df.loc[df['Volume'] > 60000])

df.loc[(df.trend == True) & (df.trend_shift == False), 'action'] = 'buy'
df.loc[(df.trend == False) & (df.trend_shift == True), 'action'] = 'sell'

df.loc[df.action == 'buy', 'marker_position'] = df['Low'] * 0.95
df.loc[df.action == 'sell', 'marker_position'] = df['High'] * 1.05

print(df[df.marker_position.notnull()])

buy_dataFrame = df.loc[df.action == 'buy']
sell_dataFrame = df.loc[df.action == 'sell']

print(buy_dataFrame)

print(sell_dataFrame)

plt.figure(figsize=(16, 9))
plt.plot(df.Close, label='Close Price')
plt.plot(df.ema_short, label='EMA 12')
plt.plot(df.ema_long, label='EMA 26')
plt.plot(buy_dataFrame.marker_position, 'g^', markersize=10)
plt.plot(sell_dataFrame.marker_position, 'rv', markersize=10)
plt.legend()


markers = ['^' if x == 'buy' else ('v' if x == 'sell' else 'o') for x in df['action']]
color_marker = ['green' if x == 'buy' else 'red' for x in df['action']]
plot_signal = mpf.make_addplot(df['marker_position'], type='scatter', markersize=30, marker=markers, color=color_marker)

mpf.plot(df, type='candle', style='yahoo', addplot=[ema_short, ema_long, plot_signal], figsize=(16, 9))

df['action_price'] = df['Open'].shift(-1)
print(df.head())

df_txn = df[df.action.notnull()]

df_txn['return'] = df_txn['action_price'].pct_change()

print(df_txn)

df_txn = df_txn.iloc[1:, :]

print(df_txn)

profit = df_txn[df_txn.action == 'sell']

print(profit)

profit['return'].plot(kind='bar', figsize=(16, 9), title='Profit')