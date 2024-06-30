from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.technical_indicators import SMA, EMA, STDEV, ATR

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the stocks to trade.
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
        # Define leverage for scalping trades.
        self.leverage = 2

    @property
    def assets(self):
        # Return the list of tickers we are interested in.
        return self.tickers
    
    @property
    def interval(self):
        # Define the polling interval as 5 minutes for high-frequency trading
        return "5min"
    
    def run(self, data):
        allocation_dict = {}
        # Iterate through each ticker
        for ticker in self.tickers:
            # Get the necessary data for the current ticker.
            # Calculate simple moving average (SMA) & Exponential Moving Average (EMA) for short and long periods.
            short_sma = SMA(ticker, data["ohlcv"], length=5)
            long_sma = SMA(ticker, data["ohlcv"], length=20)
            short_ema = EMA(ticker, data["ohlcv"], length=5)
            long_ema = EMA(ticker, data["ohlcv"], length=20)
            atr = ATR(ticker, data["ohlcv"], length=14)[-1] # Average True Range for volatility
            
            # Establish entry strategy
            if short_sma[-1] > long_sma[-1] and short_ema[-1] > long_ema[-1]:
                # Simple resistance break scalping strategy
                allocation_dict[ticker] = 1.0 / len(self.tickers) * self.leverage
            else:
                # No position or exit strategy, assuming scalping means frequent entries and exits.
                allocation_dict[ticker] = 0
        
        return TargetAllocation(allocation_dict)