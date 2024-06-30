from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # The ticker symbol for the asset you're trading
        self.ticker = "AAPL"

    @property
    def assets(self):
        # Define the assets this strategy will operate on
        return [self.ticker]

    @property
    def interval(self):
        # Defines the interval for the market data; adjust based on your strategy needs
        return "5min"

    def run(self, data):
        # This method implements the trading logic for support/resistance levels

        # Initialize allocation for the asset
        allocation = {self.ticker: 0}

        # Fetch the ohlcv (open-high-low-close-volume) data for the ticker
        ohlcv = data["ohlcv"]

        # Ensure there's enough data to compute technical indicators
        if len(ohlcv) < 20:  # Example threshold; adjust based on your indicators
            return TargetAllocation(allocation)

        # Calculate Bollinger Bands as potential resistance (upper band) and support (lower band) indicators
        bollinger_bands = BB(self.ticker, ohlcv, 20, 2)  # using a 20-day window & 2 standard deviations
        
        # Access the latest price data
        latest_close = ohlcv[-1][self.ticker]['close']

        # Strategy Logic:
        # If the price is near the lower Bollinger Band, consider it as near support level and buy
        if latest_close <= bollinger_bands['lower'][-1]:
            log("The price is near the support level; considering buying.")
            allocation[self.ticker] = 1  # Allocating 100% to this asset as a buy signal

        # If the price is near the upper Bollinger Band, consider it as near resistance level and sell
        elif latest_i_close >= bollinger_bands['upper'][-1]:
            log("The price is near the resistance level; considering selling.")
            allocation[self.ticker] = 0  # Setting allocation to 0% as a sell signal

        # If the price is between the bands, no clear signal, maintain previous positions or stay neutral
        else:
            log("The price is between support and resistance levels; doing nothing.")

        return TargetAllocation(allocation)