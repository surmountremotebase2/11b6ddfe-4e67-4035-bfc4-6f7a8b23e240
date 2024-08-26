from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # We're interested in tracking the SPY as a proxy for S&P 500 performance
        return ["SPY"]

    @property
    def interval(self):
        # Daily intervals to analyze the broader trend
        return "1day"

    def run(self, data):
        # Initialize SPXS stake to 0; we only want to hold it under certain conditions
        spxs_stake = 0
        # Analyze SPY data to get MACD indicators
        spy_macd = MACD("SPY", data["ohlcv"], fast=12, slow=26)
        
        if spy_macd is not None:
            # Get MACD and Signal line lists
            macd_line, signal_line = spy_macd["MACD"], spy_macd["signal"]
            # If the MACD line crosses above the signal line, it's a bullish signal for the SPY
            # This means we expect SPXS to drop, presenting a short opportunity
            if len(macd_line) > 1 and len(signal_line) > 1:
                if macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]:
                    log("Bullish MACD crossover for SPY. Considering short position in SPXS.")
                    # Aggressive short; adjust magnitude according to strategy risk preference
                    spxs_stake = 1  # 1 indicates a full allocation according to strategy. This could be adjusted for leverage.
                else:
                    log("No bullish crossover signal. Avoiding SPXS position.")
        else:
            log("Unable to calculate MACD for SPY.")

        # Utilizing the TargetAllocation structure to indicate our position decision
        return TargetAllocation({"SPXS": spxs_stake})