from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define a list of stock tickers to trade on
        self.tickers = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN"]
        # Define the window size for resistance calculation
        self.window_size = 10

    @property
    def interval(self):
        # Set the strategy to operate on an intraday frequency, adjust as needed
        return "5min"

    @property
    def assets(self):
        # Return the list of tickers this strategy will operate on
        return self.tickers

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            if not data.get("ohlcv"):
                # Skip if there's no data available
                continue

            # Fetch high prices for the ticker from the data
            highs = [x[ticker]["high"] for x in data["ohlcv"]]
            # Ensure there's enough data to apply the strategy
            if len(highs) < self.window_size:
                continue
            
            # Calculate current resistance level as the highest price in the defined window
            resistance = max(highs[-self.window_size:])

            # Get the last closing price for the ticker
            last_close_price = data["ohlcv"][-1][ticker]["close"]

            # Compare the last closing price to the resistance level
            if last_close_price > resistance:
                # If the price has broken through the resistance, allocate a portion of the portfolio to this stock
                allocation_dict[ticker] = 0.2  # Allocate 20%, customize as needed
            else:
                # If the price is below the resistance, do not allocate (or exit the position)
                allocation_dict[ticker] = 0

        # Optimize allocation (ensure total allocation does not exceed 100%)
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            # Normalize allocations if total exceeds 100%
            allocation_dict = {k: v / total_allocation for k, v in allocation_dict.items()}

        return TargetURRENCYAllocation(allocation_dict)