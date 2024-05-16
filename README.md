# Stock_Insights

This project detects various candlestick patterns in stock market data using Python and pandas. The patterns include Doji, Engulfing, Hammer, Hanging Man, Morning Star, Evening Star, and Shooting Star.

## Usage

1. **Prepare Data**: Ensure your CSV file has columns `Date`, `Open`, `High`, `Low`, `Close`. Optionally, include `Adj Close` and `VWAP`.

2. **Detect Patterns**:
   - Doji and Engulfing: `python doji_engulfing.py`
   - Hammer and Inverted Hammer: `python hammers.py`
   - Hanging Man: `python hanging_man.py`
   - Morning Star, Evening Star, Shooting Star: `python stars.py`

3. **Results**: Each script generates a new CSV file with detected patterns.

## Requirements

- Python 3.x
- pandas

## Contributing

Contributions are welcome! Submit a pull request or open an issue.

## License

This project is licensed under the MIT License.
