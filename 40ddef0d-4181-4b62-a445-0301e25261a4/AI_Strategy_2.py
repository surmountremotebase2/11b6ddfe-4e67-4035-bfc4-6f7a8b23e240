from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # We focus solely on SPXS, the inverse S&P 500 leveraged ETF
        self.tickers = ["SPXS"]
    
    @property
    def interval(self):
        # Daily data to analyze the market trend
        return "1day"
    
    @property
    def assets(self):
        # Only trading on SPXS
        return self.tickers
    
    def run(self, data):
        # Initialize allocation with no investment
        allocation_dict = {"SPXS": 0.0}
        
        d = data["ohlcv"]
        
        if len(d) > 14:  # Ensuring we have enough data for analysis
            # Calculate the 14-day RSI for SPXS
            rsi_values = RSI("SPXS", d, 14)
            # Calculate the 50-day simple moving average for SPXS
            sma_values = SMA("SPXS", d, 50)
            
            current_price = d[-1]["SPXS"]["close"]
            rsi_current = rsi_values[-1]
            sma_current = sma_values[-1]
            
            # Decision logic:
            # If the RSI is above 70, it's often considered overbought - however, as this is an inverse ETF, 
            # an overbought condition might actually signal a strong bearish sentiment for the S&P 500,
            # warranting an aggressive position.
            # We also check if the current price is below the 50-day SMA as a confirmation.
            if rsi_current > 70 and current_price < sma_current:
                log("Aggressively buying SPXS as it is overbought but below the SMA, indicating a bearish sentiment.")
                allocation_dict["SPXS"] = 1.0  # Putting 100% of our portfolio into SPXS
            
            # Note: This is a highly aggressive and risky strategy suitable for short time frames.
            # Always backtest strategies like these with historical data to understand potential performance and risk.
        
        return TargetAllocation(allocation_dict)