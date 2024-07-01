from surmount.base_class import Strategy, TargetAllocation
from surmount.data import InsiderTrading

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize with a list of 100 stock tickers
        self.tickers = ["AAPL", "MSFT", "GOOGL"] # Add more tickers to reach 100
        # Prepare InsiderTrading data requests for all tickers
        self.data_list = [InsiderTrading(i) for i in self.tickers]

    @property
    def interval(self):
        # Define the data interval (daily for this case)
        return "1day"

    @property
    def assets(self):
        # Declare which assets are included in this strategy
        return self.tickers

    @property
    def data(self):
        # Data to be used in the strategy: insider trading data for the tickers
        return self.data_list

    def run(self, data):
        # Initialize allocation dictionary with zero allocation for each ticker
        allocation_dict = {i: 0 for i in self.tickers}
        
        # Loop through each piece of insider trading data
        for i in self.data_list:
            data_key = tuple(i)
            
            # Check for any insider trading data available
            if data_key in data and len(data[data_key]) > 0:
                # Analyze the latest insider transactions for each ticker
                last_transaction = data[data_key][-1]
                
                # Strategy: Avoid stocks with recent insider sales, equally invest in others.
                # This simplistic logic could be expanded with more nuanced conditions.
                if "Sale" not in last_transaction['transactionType']:
                    allocation_dict[data_key[1]] = 1/len([ticker for ticker, transactions in allocation_dict.items() if transactions >= 0])

        # Return target allocation based on the strategy logic
        return TargetAllocation(allocation_dict)