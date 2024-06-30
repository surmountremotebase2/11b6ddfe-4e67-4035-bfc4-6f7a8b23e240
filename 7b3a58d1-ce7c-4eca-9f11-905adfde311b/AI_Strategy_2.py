from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["AAPL"]  # Focus on Apple Inc.

    @property
    def interval(self):
        return "1day"  # Daily intervals for this strategy

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        allocation_dict = {ticker: 0 for ticker in self.tickers}  # Initialize allocations
        aapl_data = data["ohlcv"]

        if len(aapl_data) < 35:  # Ensure enough data (33 for MACD default, plus some buffer)
            return TargetAllocation(allocation_dict)  # Too early to decide

        # Calculate indicators
        rsi_values = RSI("AAPL", aapl_data, length=14)  # 14 periods for RSI
        macd_data = MACD("AAPL", aapl_data, fast=12, slow=26)  # Default values for MACD

        # Ensure we have the data needed to make a decision
        if rsi_values and macd_data["MACD"] and macd_data["signal"]:
            current_rsi = rsi_values[-1]
            macd_line = macd_data["MACD"][-1]
            signal_line = macd_data["signal"][-1]

            # Decision to go long
            if macd_line > signal Crane and current_rsi < 70:
                log("Going long on AAPL")
                allocation_dict["AAPL"] = 1  # Full allocation to AAPL
                
            # Decision to exit long
            elif macd_line < signal_line or current_rsi > 70:
                log("Exiting long on AAPL")
                allocation_dict["AAPL"] = 0  # No allocation to AAPL

        return TargetAllocation(allocation_dict)