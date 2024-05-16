import pandas as pd
import numpy as np

# Read stock data from CSV
stock_data = pd.read_csv('Stock_Insights/stock.csv')

# Function to classify a candle as bullish, bearish, or indecisive
def classify_candle(candle):
    if candle['Close'] > candle['Open']:
        return 'Bullish'
    elif candle['Close'] < candle['Open']:
        return 'Bearish'
    else:
        return 'Indecisive'

# Function to identify local minima
def find_local_minima(data, window=3):
    data['Local_Min'] = data['Low'][(data['Low'] < data['Low'].shift(1)) & (data['Low'] < data['Low'].shift(-1))]
    return data

# Function to identify hammer patterns
def identify_hammer(candle, prev_candle):
    body_size = abs(candle['Close'] - candle['Open'])
    upper_shadow = candle['High'] - max(candle['Close'], candle['Open'])
    lower_shadow = min(candle['Close'], candle['Open']) - candle['Low']
    
    # Hammer criteria: Lower shadow is at least 2 times the body, upper shadow is minimal
    if body_size <= lower_shadow * 0.3 and upper_shadow <= body_size * 0.2:
        # Ensure it follows a downtrend (previous candle had higher close)
        if prev_candle['Close'] > candle['Close']:
            return 'Hammer'
    # Inverted Hammer criteria: Upper shadow is at least 2 times the body, lower shadow is minimal
    elif body_size <= upper_shadow * 0.3 and lower_shadow <= body_size * 0.2:
        # Ensure it follows a downtrend (previous candle had higher close)
        if prev_candle['Close'] > candle['Close']:
            return 'Inverted Hammer'
    return None

# Classify candle types
stock_data['Candle_Type'] = stock_data.apply(classify_candle, axis=1)

# Find local minima
stock_data = find_local_minima(stock_data)

# Initialize a list to store patterns
patterns = []

# Loop through the stock data to identify hammer patterns
for i in range(1, len(stock_data)):
    current_candle = stock_data.iloc[i]
    prev_candle = stock_data.iloc[i - 1]
    
    # Identify hammer patterns at local minima
    if not np.isnan(current_candle['Local_Min']):
        hammer_pattern = identify_hammer(current_candle, prev_candle)
        if hammer_pattern:
            patterns.append((current_candle.name, hammer_pattern))

# Add identified patterns to the DataFrame
for idx, pattern in patterns:
    stock_data.at[idx, 'pattern'] = pattern

stock_data.to_csv('Stock_Insights/stock.csv', index=False)

print(stock_data)
