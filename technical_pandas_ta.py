import mplfinance as mpf
import yfinance as yf
import pandas as pd
import pandas_ta as ta

start = '2025-01-01'
end = '2026-01-01'

btc = yf.Ticker('BTC-USD')
data = btc.history(start=start, end=end)

print(data.ta.macd())

print(data.ta.percent_return(cummulative=True))

print(data.ta.indicators())

print(data.ta.ema(length=26))

df_ta = data.copy()
print(df_ta.ta.macd(fast=12, slow=21, signal=7))

rsi = df_ta.ta.rsi()
print(rsi)

df_ta.ta.macd(append=True)
df_ta.ta.rsi(append=True)
print(df_ta)
print(df_ta.columns)
df_ta.columns = ["Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits", "macd",
                 "histogram", "signal_line", "rsi"]
print(df_ta.columns)

# Plot Graph with macd/rsi
mpf_macd = mpf.make_addplot(df_ta['macd'], panel=1, color='blue', ylabel='MACD')
mpf_signal = mpf.make_addplot(df_ta['signal_line'], panel=1, color='orange')

colors = ['green' if x >= 0 else 'red' for x in df_ta['histogram']]
mpf_histogram = mpf.make_addplot(df_ta['histogram'], type='bar', panel=1, color=colors)

mpf_rsi = mpf.make_addplot(df_ta['rsi'], panel=2, color='blue', ylabel='RSI')

ta_plot = [mpf_macd, mpf_histogram, mpf_signal, mpf_rsi]

mpf.plot(df_ta, type='candle', style='default', addplot=ta_plot, tight_layout=True, panel_ratios=(3,1,1), figratio=(2,1), figscale=1.5)

# draw line in price panel

mpf.plot(df_ta, type='candle', style='default', addplot=ta_plot, tight_layout=True, panel_ratios=(3,1,1), figratio=(2,1),
         figscale=1.5, hlines=dict(hlines=[120000, 80000], colors=['r', 'g'], linestyle='-'))

# draw line in rsi panel

df_ta['rsi_upper'] = 70
df_ta['rsi_lower'] = 30

mpf_rsi_upper = mpf.make_addplot(df_ta['rsi_upper'], panel=2, color='green')
mpf_rsi_lower = mpf.make_addplot(df_ta['rsi_lower'], panel=2, color='red')
ta_plot = [mpf_macd, mpf_histogram, mpf_signal, mpf_rsi, mpf_rsi_upper, mpf_rsi_lower]

mpf.plot(df_ta, type='candle', style='default', addplot=ta_plot, tight_layout=True, panel_ratios=(3,1,1), figratio=(2,1), figscale=1.5)