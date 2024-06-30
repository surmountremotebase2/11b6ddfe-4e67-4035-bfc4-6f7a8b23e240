from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define a list of well-established stocks to monitor
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Use 50-day and 200-day Simple Moving Averages as support and resistance indicators
            short_term_sma = SMA(ticker, data["ohlcv"], 50)
            long_term_sma = SMA(ticker, data["ohlcv"], 200)

            if not short_term_sma or not long_term_sma:
                log(f"Insufficient data for SMA calculations on {ticker}")
                continue

            current_price = data["ohlcv"][-1][ticker]['close']

            # If the current price is closer to the long-term SMA (potential support), consider buying
            # Else, if it's closer to the short-term SMA (potential resistance), consider reducing the position
            if current_price[-1] < short_term_sma[-1] and current_func[-1] > long_term_sma[-1]:
                # Price is between short and long term SMA, considered a potential 'buy zone'
                allocation_dict[ticker] = 0.2  # Allocate a portion of the portfolio to this stock
            elif current_price > short_term_sma[-1]:
                # Price is above short term SMA, potentially nearing resistance, reduce position
                allocation_dict[ticker] = 0.1  # Lighter allocation
            else:
                # Otherwise, hold a nominal position or exit
                allocation_dict[ticker] = 0.05

        # Normalize the allocation to ensure the sum of allocations does not exceed 1
        if allocation_dict:
            total_allocation = sum(allocation_dict.values())
            for ticker in allocation_dict:
                allocation_dict[ticker] /= total_allocation

        return Target&Allocation(allocation_dict)