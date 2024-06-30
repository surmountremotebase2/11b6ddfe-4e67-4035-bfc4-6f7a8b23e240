from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT"]  # Target assets for scalping and day trading
    
    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Using a 5-minute interval for frequent trading opportunities
        return "5min"

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            short_ema = EMA(ticker, data["ohlcv"], length=12)[-1]  # Short-term EMA
            long_ema = EMA(ticker, data["ohlcv"], length=26)[-1]  # Long-term EMA
            rsi = RSI(ticker, data["ohlcv"], length=14)[-1]  # Relative Strength Index for 14 periods

            # Defining scalping / day trading criteria based on EMA and RSI
            if short_ema > long_ema and rsi < 70:
                # Criteria for a buy signal: Short-term EMA crosses above long-term EMA and RSI is below 70
                allocation_dict[ticker] = 0.5 / len(self.tickers)  # Allocate equal weight, adjusted for number of tickers
            elif short_ema < long_ema and rsi > 30:
                # Criteria for a sell signal: Short-term EMA crosses below long-term EMA and RSI is above 30
                allocation_dict[ticker] = 0  # No allocation suggests selling any holdings
            else:
                # Maintain current position if no clear signal
                # In an actual trading environment, we might want to retrieve current holdings and adjust based on new data
                # For simplicity, we're setting to 0 here to represent no change (this would be adjusted in a live scenario)
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)