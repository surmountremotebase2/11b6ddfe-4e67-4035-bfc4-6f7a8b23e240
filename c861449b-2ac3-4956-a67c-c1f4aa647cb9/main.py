from surmount.base_class import Strategy, TargetAllocation
from surmount.data import InsiderTrading

class TradingStrategy(Strategy):
    def __init__(self):
        # List of tickers to monitor for insider trading activities
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
        # Create an InsiderTrading data object for each ticker
        self.data_list = [InsiderTrading(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        # Setting the interval property to daily
        return "1day"

    @property
    def assets(self):
        # Specifying the assets that the strategy will consider
        return self.tickers
    
    @property
    def data(self):
        # Returning the list of data objects (InsiderTrading)
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for i in self.data_list:
            # Checking for the most recent insider trade for each asset
            recent_trade = data[tuple(i)].pop() if data[tuple(i)] else None
            if recent_trade:
                if recent_trade['transactionType'] == "Purchase":
                    # If the latest insider trade is a purchase, allocate a portion of the portfolio to this stock
                    allocation_dict[tuple(i)[1]] = 1.0 / len(self.tickers)
                else:
                    # If the latest insider trade is not a purchase (e.g., sale), do not allocate any to this stock
                    allocation_dict[tuple(i)[1]] = 0
            else:
                # If there is no recent trade data, set allocation to zero
                allocation_dict[tuple(i)[1]] = 0

        return TargetAllocation(allocation_dict)