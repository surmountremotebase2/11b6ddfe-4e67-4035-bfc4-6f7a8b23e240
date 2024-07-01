from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the futures contract ticker you want to trade.
        # Ensure your data provider supports futures data for this ticker.
        self.ticker = "ES_F"  # Example using S&P 500 E-Mini futures
        self.short_window = 50  # Short-term SMA window
        self.long_window = 200  # Long-term SMA window

    @property
    def interval(self):
        # The data interval for SMA calculation, e.g., daily.
        return "1day"

    @property
    def assets(self):
        # List of assets the strategy trades, in this case, just one.
        return [self.ticker]

    def run(self, data):
        # Extract closing prices for the ticker
        closes = [d[self.ticker]["close"] for d in data["ohlcv"]]

        # Calculate short-term and long-term SMAs
        short_sma = SMA(self.ticker, data["ohlcv"], self.short_window)
        long_sma = SMA(self.ticker, data["ohlcv"], self.long_window)

        if len(short_sma) == 0 or len(long_sma) == 0:
            return TargetAllocation({self.ticker: 0})  # No action if insufficient data

        # The latest SMA values
        current_short_sma = short_sma[-1]
        current_long_sma = long_sma[-1]

        # Determine the trading signal
        if current_short_sma > current_long_sma:
            # Positive momentum - go long
            allocation = 1.0
        elif current_short_sma < current_long_sma:
            # Negative momentum - exit or go short depending on your strategy
            allocation = 0.0  # This strategy exits the position; adjust based on your risk preference
        else:
            # No clear signal
            allocation = 0.0

        return TargetAllocation({self.ticker: allocation})