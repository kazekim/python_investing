import pandas as pd
import mplfinance as mpf
import yfinance as yf

start = '2025-01-01'
end = '2026-01-01'

btc = yf.Ticker('BTC-USD')
data = btc.history(start=start, end=end)

print(data)

data.Close.plot()

df = data.iloc[:, :-1]

print(df)

EMA_short = df['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
EMA_long = df['Close'].ewm(span=26, adjust=False, min_periods=26).mean()

MACD = EMA_short - EMA_long

print(MACD)

signal = MACD.ewm(span=9, adjust=False, min_periods=9).mean()

df['macd'] = MACD
df['signal_line'] = signal
df['histogram'] = df['macd'] - df['signal_line']

df['shift_histogram'] = df['histogram'].shift(1)

print(df)

# histogram ตัดขึ้น
df[df['histogram'] > 0 & (df['shift_histogram'] < 0)]

#กรอง trend ขาขึ้น
df['trend'] = df['macd'] > df['signal_line']

df.loc[(df['trend'] == True) & (df['trend'].shift() == False), "action"] = 'buy'
df.loc[(df['trend'] == False) & (df['trend'].shift() == True), "action"] = 'sell'

print(df[df['action'].notnull()])

# Visualization
mpf_macd = mpf.make_addplot(df['macd'], panel=1, color='blue', title='MACD')
mpf_signal = mpf.make_addplot(df['signal_line'], panel=1, color='orange')

colors = ['green' if value >= 0 else 'red' for value in df['histogram']]
mpf_histogram = mpf.make_addplot(df['histogram'], type='bar', panel=1, color=colors)

macd_plot = [mpf_macd, mpf_signal, mpf_histogram]

print(type(mpf_histogram))

print(type(macd_plot))

mpf.plot(df, type='candle', style='yahoo', addplot=macd_plot)

print(df[df.action.notnull()])

df['action_price'] = df['Open'].shift(-1)

df_txn = df[df.action.notnull()]

print(df_txn)

df_txn['return'] = df_txn['action_price'].pct_change()

print(df_txn)

# play sell only profit
df_txn[df_txn['action'] == 'sell']['return'].plot(kind='bar')

# play buy only profit
# df_txn[df_txn['action'] == 'buy']['return'].plot(kind='bar')


df.loc[df['action'] == 'buy', 'marker_position'] = df['Low'] * 0.95
df.loc[df['action'] == 'sell', 'marker_position'] = df['High'] * 1.05

# for buy, sell signal
markers = ['^' if x == 'buy' else 'v' for x in df['action']]
color_marker = ['green' if x == 'buy' else 'red' for x in df['action']]
plot_signal = mpf.make_addplot(df['marker_position'], type='scatter', marker=markers, color=color_marker)

print(type(plot_signal))

all_plot = macd_plot + [plot_signal]

mpf.plot(df, type='candle', style='yahoo', addplot=all_plot)