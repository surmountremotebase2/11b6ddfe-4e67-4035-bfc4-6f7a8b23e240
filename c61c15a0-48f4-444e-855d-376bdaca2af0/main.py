from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Choose assets for trading
        self.tickers = ["SPY", "QQQ"]
        
    @property
    def interval(self):
        # Set the data fetch interval to daily
        return "5min"
    
    @property
    def assets(self):
        # List of assets this strategy trades
        return self.tickers

    @property
    def data(self):
        # Data required by the strategy
        return []

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Calculate the Bollinger Bands for each asset
            bollinger_bands = BB(ticker, data["ohlcv"], 20)
            if bollinger_bands is not None:
                current_price = data["ohlcv"][-1][ticker]['close']
                # Check if the current price is touching the upper band (resistance)
                if current_price >= bollinger_bands['upper'][-1]:
                    # If touching resistance, prepare to short sell, here we just sell
                    allocation_dict[ticker] = 0  # 0 allocation represents a sell signal
                elif current_price <= bollinger_bands['lower'][-1]:
                    # If touching lower band (support), buy or increase position
                    allocation_dict[ticker] = 1 / len(self.tickers)  # Equally divided allocation among tickers
                else:
                    # If within bands, do nothing
                    allocation_dict[ticker] = allocation_dict.get(ticker, 0)
            else:
                # If Bollinger Bands can't be calculated, do nothing
                allocation_dict[ticker] = allocation_dict.get(ticker, 0)
        
        # Log the allocation decision
        log("Allocations: " + str(allocation_dict))
        
        return TargetAllocation(allocation_dict)