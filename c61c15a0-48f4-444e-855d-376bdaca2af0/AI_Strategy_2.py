from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, MAX
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers for the five different stocks
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        # Determine the lookback period for calculating resistance
        self.lookback_period = 14
    
    @property
    def interval(self):
        # Day trading strategy, so '1day' interval for data
        return "1day"

    @property
    def assets(self):
        # Return the list of stock tickers to be traded
        return self.tickers
        
    def run(self, data):
        allocation_dict = {}
        
        # Iterate through each stock to determine its target allocation
        for ticker in self.tickers:
            # Get historical closing prices
            closing_prices = [d[ticker]["close"] for d in data["ohlcv"]]
            
            # Calculate the maximum close price over the lookback period
            resistance_level = MAX(ticker, data["ohlcv"], self.lookback_period)
            
            # Current price for decision-making
            current_price = closing_prices[-1] if len(closing_data) > 0 else None
            
            # Simple strategy to buy if the current price is close to the resistance level
            # and assuming the resistance level might act as a support
            if current_price and resistance_level and current_price >= resistance_level * 0.98:
                # Assign equal weight if the condition meets, here assuming a simplistic equal distribution
                allocation_dict[ticker] = 1.0/len(self.tickers)
            else:
                # Do not allocate to stocks not meeting the criteria
                allocation_dict[ticker] = 0
        
        # Log the allocation decision
        log(f"Allocation: {allocation_dict}")
        
        # Return the target allocation based on the logic above
        return TargetAllocation(allocation_dict)