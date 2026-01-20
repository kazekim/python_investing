import yfinance as yf
import pandas as pd
import pandas_ta as ta

start = '2025-01-01'
end = '2026-01-01'

btc = yf.Ticker('BTC-USD')
data = btc.history(start=start, end=end)
df = data.copy()

CustomStrategy = ta.Strategy(
    name='Custom Strategy',
    description='Custom strategy description',
    ta=[{"kind": "ema", "length": 12},
        {"kind": "ema", "length": 26},
        {"kind": "macd", "fast": 12, "slow": 21},
        {"kind": "rsi"}]
)

df.ta.strategy(CustomStrategy)

print(df)

df['MACD_trend'] = df['MACD_12_21_9'] > df['MACDs_12_21_9']

df.loc[(df['MACD_Trend'] == True) & (df['MACD_Trend'].shift() == False) & (df['RSI_14'] < 30), 'action'] = 'buy'

print(df[df.action == 'buy'].iloc[:, -5:])

df.loc[(df['MACD_Trend'] == False) & (df['MACD_Trend'].shift() == True) & (df['RSI_14'] > 70), 'action'] = 'sell'

print(df[df.action.notnull()].iloc[:, -5:])
