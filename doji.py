import pandas as pd

stock_data = pd.read_csv('ADANI_ENTERPRISES.csv')

def classify_candle(candle):
    if candle['Close'] > candle['Open']:
        return 'Bullish'
    elif candle['Close'] < candle['Open']:
        return 'Bearish'
    else:
        return 'Indecisive'
    
def isDoji(candle):
    if candle['Candle_Type'] == 'Bullish':
        if 20 * abs(candle['Open'] - candle['Close']) <= candle['High'] - candle['Low']:
            return 'Doji'
    elif candle['Candle_Type'] == 'Bearish':
        if 20 * abs(candle['Open'] - candle['Close']) <= candle['High'] - candle['Low']:
            return 'Doji'
    elif candle['Candle_Type'] == 'Indecisive':
        return 'Doji'
    return None 

stock_data.drop(['Adj Close', 'VWAP'], axis=1, inplace=True)


stock_data['Candle_Type'] = stock_data.apply(classify_candle, axis=1)
stock_data['pattern'] = stock_data.apply(isDoji, axis=1)

stock_data.to_csv('stock.csv', index=False)
