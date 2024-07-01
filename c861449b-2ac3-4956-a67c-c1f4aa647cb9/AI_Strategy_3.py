# Import necessary components from Surmount AI's package
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # The futures we are interested in
        self.tickers = ["ES", "NQ"]

    @property
    def interval(self):
        # Use daily data for analysis
        return "1day"
    
    @property
    def assets(self):
        # Define the futures to apply the strategy
        return self.tickers

    def run(self, data):
        # Initialize allocation for each future
        allocation_dict = {"ES": 0, "NQ": 0}

        # Computing the Short-Term and Long-Term SMAs for each future
        es_sma_short = SMA("ES", data["ohlcv"], length=10) # Short-term SMA
        es_sma_long = SMA("ES", data["ohlcv"], length=50)  # Long-term SMA

        nq_sma_short = SMA("NQ", data["ohlcv"], length=10)
        nq_sma_long = SMA("NQ", data["ohlcv"], length=50)

        if es_sma_short[-1] > es_sma_long[-1] and nq_sma_short[-1] < nq_sma_long[-1]:
            # If ES's short SMA is above its long SMA and NQ's short SMA is below its long SMA,
            # allocate 100% to ES (go long) and 0% to NQ
            allocation_dict["ES"] = 1.0
            allocation_dict["NQ"] = 0
        elif es_sma_short[-1] < es_sma_long[-1] and nq_sma_short[-1] > nq_sma_long[-1]:
            # If ES's short SMA is below its long SMA and NQ's short SMA is above its long SMA,
            # allocate 0% to ES and 100% to NQ (go long)
            allocation_dict["ES"] = 0
            allocation_dict["NQ"] = 1.0

        # Print allocation for logging purposes
        log(f"Allocation: {allocation_dict}")

        # Return the target allocation
        return TargetAllocation(allocation_dict)