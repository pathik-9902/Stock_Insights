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

# Function to identify local maxima and minima
def find_local_extrema(data, window=3):
    data['Local_Max'] = data['High'][(data['High'] > data['High'].shift(1)) & (data['High'] > data['High'].shift(-1))]
    data['Local_Min'] = data['Low'][(data['Low'] < data['Low'].shift(1)) & (data['Low'] < data['Low'].shift(-1))]
    return data

# Function to identify Morning Star patterns
def identify_morning_star(candles):
    if len(candles) != 3:
        return None
    first, second, third = candles
    if (first['Candle_Type'] == 'Bearish' and 
        second['Low'] < first['Close'] and second['High'] < first['Open'] and 
        third['Candle_Type'] == 'Bullish' and third['Close'] > first['Open']):
        return 'Morning Star'
    return None

# Function to identify Evening Star patterns
def identify_evening_star(candles):
    if len(candles) != 3:
        return None
    first, second, third = candles
    if (first['Candle_Type'] == 'Bullish' and 
        second['High'] > first['Close'] and second['Low'] > first['Open'] and 
        third['Candle_Type'] == 'Bearish' and third['Close'] < first['Open']):
        return 'Evening Star'
    return None

# Function to identify Shooting Star patterns
def identify_shooting_star(candle, prev_candle):
    body_size = abs(candle['Close'] - candle['Open'])
    upper_shadow = candle['High'] - max(candle['Close'], candle['Open'])
    lower_shadow = min(candle['Close'], candle['Open']) - candle['Low']
    
    # Shooting Star criteria: Upper shadow is at least 2 times the body, lower shadow is minimal
    if body_size <= upper_shadow * 0.3 and lower_shadow <= body_size * 0.2:
        # Ensure it follows an uptrend (previous candle had lower close)
        if prev_candle['Close'] < candle['Close']:
            return 'Shooting Star'
    return None

# Classify candle types
stock_data['Candle_Type'] = stock_data.apply(classify_candle, axis=1)

# Find local extrema
stock_data = find_local_extrema(stock_data)

# Initialize a list to store patterns
patterns = []

# Loop through the stock data to identify patterns
for i in range(2, len(stock_data)):
    current_candle = stock_data.iloc[i]
    prev_candle = stock_data.iloc[i - 1]
    prev_prev_candle = stock_data.iloc[i - 2]
    
    # Identify Morning Star patterns at local minima
    if not np.isnan(current_candle['Local_Min']):
        morning_star_pattern = identify_morning_star([prev_prev_candle, prev_candle, current_candle])
        if morning_star_pattern:
            patterns.append((current_candle.name, morning_star_pattern))
    
    # Identify Evening Star patterns at local maxima
    if not np.isnan(current_candle['Local_Max']):
        evening_star_pattern = identify_evening_star([prev_prev_candle, prev_candle, current_candle])
        if evening_star_pattern:
            patterns.append((current_candle.name, evening_star_pattern))
    
    # Identify Shooting Star patterns at local maxima
    if not np.isnan(current_candle['Local_Max']):
        shooting_star_pattern = identify_shooting_star(current_candle, prev_candle)
        if shooting_star_pattern:
            patterns.append((current_candle.name, shooting_star_pattern))

# Add identified patterns to the DataFrame
for idx, pattern in patterns:
    stock_data.at[idx, 'pattern'] = pattern

# Save the modified DataFrame to a new CSV file
stock_data.to_csv('Stock_Insights/stock.csv', index=False)

# Print the DataFrame to check the results
print(stock_data)
