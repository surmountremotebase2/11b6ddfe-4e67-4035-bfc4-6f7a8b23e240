from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import Asset, OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the futures to trade
        self.futures = ["ES1", "NQ1", "CL1", "GC1", "SI1", "EUR1", "GBP1", "JPY1", "AUD1", "CAD1"]
        # Generate OHLCV data requests for each future
        self.data_list = [OHLCV(future) for future in self.futures]

    @property
    def interval(self):
        # Set the data interval
        return "1day"

    @property
    def assets(self):
        # Return the list of futures to trade
        return self.futures

    @property
    def data(self):
        # Return the list of data required for the strategy
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for future in self.futures:
            # Ensure we have enough data points for our calculation
            if len(data["ohlcv"][future]) < 50:  # Assuming we need at least 50 days for the long SMA
                log(f"Not enough data for {future}")
                continue

            # Calculate short-term (10 days) and long-term (50 days) SMAs
            short_sma = SMA(future, data["ohlcv"][future], length=10)
            long_sma = SMA(future, data["ohlcv"][future], length=50)

            # Implement the trading signal logic
            if short_sma[-1] > long_sma[-1]:
                log(f"Going long on {future}")
                allocation_dict[future] = 0.1  # Allocate 10% to each future we go long on
            elif short_sma[-1] < long_sma[-1]:
                log(f"Closing position / staying out on {future}")
                allocation_dict[future] = 0  # No allocation if the short SMA is below the long SMA

        # Return the target allocation for each future
        return TargetAllocation(allocation_dict)