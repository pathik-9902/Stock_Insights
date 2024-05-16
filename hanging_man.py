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

# Function to identify local maxima
def find_local_maxima(data, window=3):
    data['Local_Max'] = data['High'][(data['High'] > data['High'].shift(1)) & (data['High'] > data['High'].shift(-1))]
    return data

# Function to identify hanging man patterns
def identify_hanging_man(candle, prev_candle):
    body_size = abs(candle['Close'] - candle['Open'])
    upper_shadow = candle['High'] - max(candle['Close'], candle['Open'])
    lower_shadow = min(candle['Close'], candle['Open']) - candle['Low']
    
    # Hanging Man criteria: Lower shadow is at least 2 times the body, upper shadow is minimal
    if body_size <= lower_shadow * 0.3 and upper_shadow <= body_size * 0.2:
        # Ensure it follows an uptrend (previous candle had lower close)
        if prev_candle['Close'] < candle['Close']:
            return 'Hanging Man'
    return None

# Classify candle types
stock_data['Candle_Type'] = stock_data.apply(classify_candle, axis=1)

# Find local maxima
stock_data = find_local_maxima(stock_data)

# Initialize a list to store patterns
patterns = []

# Loop through the stock data to identify hanging man patterns
for i in range(1, len(stock_data)):
    current_candle = stock_data.iloc[i]
    prev_candle = stock_data.iloc[i - 1]
    
    # Identify hanging man patterns at local maxima
    if not np.isnan(current_candle['Local_Max']):
        hanging_man_pattern = identify_hanging_man(current_candle, prev_candle)
        if hanging_man_pattern:
            patterns.append((current_candle.name, hanging_man_pattern))

# Add identified patterns to the DataFrame
for idx, pattern in patterns:
    stock_data.at[idx, 'pattern'] = pattern

# Save the modified DataFrame to a new CSV file
stock_data.to_csv('Stock_Insights/stock.csv', index=False)

# Print the DataFrame to check the results
print(stock_data)
