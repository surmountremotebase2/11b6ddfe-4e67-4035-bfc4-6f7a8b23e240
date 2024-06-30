from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers that this strategy will target.
        self.tickers = ["AAPL"]  

    @property
    def interval(self):
        # Sets the data interval to daily for calculating the RSI.
        return "1day"

    @property
    def assets(self):
        # Returns the list of assets (tickers) that the strategy will work with.
        return self.tickers

    @property
    def data(self):
        # In this strategy, direct data fetching is not defined as we rely on RSI from technical indicators. 
        # However, if specific data fetching is needed, it would be defined here.
        return []

    def run(self, data):
        """
        The core logic of the strategy, utilizing the RSI to make buying decisions.

        :param data: Contains all necessary data passed by the Surmount framework.
        :return: Target allocation object specifying how much of the portfolio is allocated to AAPL.
        """
        allocation_dict = {}

        # Calculate the RSI for AAPL.
        # Assuming a 14-day period is standard for RSI calculation.
        rsi_results = RSI("AAPL", data["ohlcv"], length=14)

        if rsi_results:
            # If RSI is below 30, it might be undervalued, suggest buying.
            if rsi_results[-1] < 30:
                log("AAPL appears oversold; consider buying.")
                allocation_dict["AAPL"] = 1.0  # Allocating 100% of the strategy budget to AAPL.
            
            # If RSI is above 70, it might be overvalued, suggesting selling or not buying more.
            elif rsi_results[-1] > 70:
                log("AAPL appears overbought; consider selling or holding.")
                allocation_dict["AAPL"] = 0  # Allocating 0% of the strategy budget to AAPL.
            else:
                # Neutral zone; no clear buy or sell signal.
                log("AAPL is neither overbought nor oversold; holding position.")
                allocation_dict["AAPL"] = 0.5  # Allocating 50% as a balanced approach
        else:
            # If there's an issue with RSI calculation, log it and do not allocate.
            log("Error calculating RSI for AAPL; no position taken.")
            allocation_dict["AAPL"] = 0

        return TargetAllocation(allocation_dict)