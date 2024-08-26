from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        self.short_ma_period = 20  # Short-term moving average period
        self.long_ma_period = 50   # Long-term moving average period
        self.asset = "AAPL"

    @property
    def assets(self):
        return [self.asset]
    
    @property
    def interval(self):
        return "1day"  # Use daily intervals for moving average calculation

    def run(self, data):
        # Calculate short-term and long-term moving averages for the asset
        short_ma = SMA(self.asset, data["ohlcv"], self.short_ma_period)
        long_ma = SMA(self.asset, data["ohlcv"], self.long_ma_period)
        
        if not short_ma or not long_ma or len(short_ma) < self.short_ma_period or len(long_ma) < self.long_ma_period:
            log("Insufficient data for calculating MAs.")
            return TargetAllocation({self.asset: 0})  # Cannot calculate MAs, so do not allocate
        
        latest_short_ma = short_ma[-1]
        latest_long_ma = long_ma[-1]
        
        # Initiate a buy signal (allocate 100% to AAPL) if the short-term MA crosses above the long-term MA
        if latest_short_ma > latest_long_ma:
            log(f"Buying signal: Short-term MA ({latest_short_ma}) crossed above Long-term MA ({latest_long_ma})")
            return TargetAllocation({self.asset: 1})  # Allocate 100% to AAPL
        
        # Initiate a sell signal (reduce allocation to 0%) if the short-term MA crosses below the long-term MA
        elif latest_short_ma < latest_long_ma:
            log(f"Selling signal: Short-term MA ({latest_short_ma}) crossed below Long-term MA ({latest_long_ma})")
            return TargetAllocation({self.asset: 0})  # Allocate 0% to AAPL
        
        # If MAs have not crossed, maintain current allocation
        else:
            log("No MA crossover detected; maintaining current allocation.")
            return TargetAllocation({self.asset: 0.5})  # Example fallback, this can be dynamic based on your strategy logic