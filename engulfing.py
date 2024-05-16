import pandas as pd

stock_data = pd.read_csv('Stock_Insights/stock.csv')

def classify_candle(candle):
    if candle['Close'] > candle['Open']:
        return 'Bullish'
    elif candle['Close'] < candle['Open']:
        return 'Bearish'
    else:
        return 'Indecisive'

def identify_engulfing(candle, prev_candle):
    if candle['Candle_Type'] == 'Bullish' and prev_candle['Candle_Type'] == 'Bearish':
        if candle['Open'] < prev_candle['Open'] and candle['Close'] > prev_candle['Close']:
            return 'Bullish Engulfing'
    elif candle['Candle_Type'] == 'Bearish' and prev_candle['Candle_Type'] == 'Bullish':
        if candle['Open'] > prev_candle['Open'] and candle['Close'] < prev_candle['Close']:
            return 'Bearish Engulfing'
    return None

stock_data['Candle_Type'] = stock_data.apply(classify_candle, axis=1)

engulfing_patterns = []

for i in range(1, len(stock_data)):
    current_candle = stock_data.iloc[i]
    previous_candle = stock_data.iloc[i - 1]
    engulfing_pattern = identify_engulfing(current_candle, previous_candle)
    if engulfing_pattern:
        engulfing_patterns.append((current_candle.name, engulfing_pattern))

for idx, pattern in engulfing_patterns:
    stock_data.at[idx, 'pattern'] = pattern

stock_data.to_csv('stock.csv', index=False)

print(stock_data)
