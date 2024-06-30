from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "NFLX", "NVDA", "BABA", "AMD"]
        # RSI Thresholds
        self.rsi_overbought = 70
        self.rsi_oversold = 30
        # MACD configuration
        self.macd_fast = 12
        self.macd_slow = 26

    @property
    def interval(self):
        return "5min"

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            rsi_value = RSI(ticker, data["ohlcv"], 14)[-1]  # Last RSI value
            macd = MACD(ticker, data["ohlcv"], self.macd_fast, self.macd_slow)
            macd_line = macd["MACD"][-1]
            signal_line = macd["signal"][-1]
            
            # Determine conditions for buying or selling
            if rsi_value > self.rsi_overbought and macd_line < signal_line:
                # Overbought conditions and MACD crossover - potential sell signal
                allocation_dict[ticker] = -0.1  # Example arbitrary short allocation, adjust based on your risk management
            elif rsi_value < self.rsi_oversold and macd_line > signal_line:
                # Oversold conditions and MACD crossover - potential buy signal
                allocation_dict[ticker] = 0.1  # Example arbitrary long allocation, adjust based on your risk management
            else:
                # Neutral, no position
                allocation_dict[ticker] = 0
        
        # Normalize allocations if necessary to ensure they do not sum over 1 or below -1 if leveraging shorts
        # This is a simplified approach and should be refined based on your risk and capital management strategies
        
        return TargetAllocation(allocation_dict)