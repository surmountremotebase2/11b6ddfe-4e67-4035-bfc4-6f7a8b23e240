from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
import numpy as np

class TradingStrategy(Strategy):
    def __init__(self):
        # Define pair of tickers for statistical arbitrage
        self.pair_tickers = ("GC AB AAAAAAAAAAAAAAAAAADEC22")
        
        # Set the lookback period for mean and standard deviation calculation
        self.lookback_short = 20  # Shorter time frame
        self.lookback_long = 60   # Longer time frame
        
    @property
    def assets(self):
        # Assets involved in the trading strategy
        return [self.pair_tickers[0], self.pair_tickers[1]] 

    @property
    def interval(self):
        # Data interval for analysis
        return "1hour"
    
    @property
    def data(self):
        # No additional data sources required for this strategy
        return []
    
    def run(self, data):
        # Fetch closing prices for both tickers
        prices_a = np.array([d[self.pair_tickers[0]]["close"] for d in data["ohlcv"] if self.pair_tickers[0] in d])
        prices_b = np.array([d[self.pair_tickers[1]]["close"] for d in data["ohlcv"] if self.pair_tickers[1] in d])
        
        if len(prices_a) < self.lookback_long or len(prices_b) < self.lookback_long:
            # Not enough data points to analyze
            return TargetAllocation({})
        
        # Compute spread = log(prices_a) - log(prices_b)
        spread = np.log(prices_a) - np.log(prices_b)
        
        # Generate signals based on mean reversion
        
        # Short term
        mean_short = np.mean(spread[-self.lookback_short:])
        std_short = np.std(spread[-self.lookback_short:])
        
        # Long term
        mean_long = np.mean(spread[-self.lookback_long:])
        std_long = np.std(spread[-self.lookback_long:])

        allocation = {}
        
        # Check if spread is mean reverting back to the longer term mean
        if spread[-1] > mean_long + std_long:
            # Spread is above long term mean -> bet on convergence
            allocation[self.pair_tickers[0]] = -0.5  # Short AAPL
            allocation[self.pair_tickers[1]] = 0.5   # Long MSFT
        elif spread[-1] < mean_long - std_long:
            # Spread is below long term mean -> bet on divergence
            allocation[self.pair_tickers[0]] = 0.5   # Long AAPL
            allocation[self.pair_tickers[1]] = -0.5  # Short MSFT
        else:
            # No clear mean reversion signal based on the current spread
            allocation[self.pair_tickers[0]] = 0
            allocation[self.pair_tickers[1]] = 0
        
    
        
        
        return TargetAllocation(allocation)