from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership, InsiderTrading

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["SPY"]
        self.data_list = [InstitutionalOwnership(i) for i in self.tickers]
        self.data_list += [InsiderTrading(i) for i in self.tickers]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        for cle in data.keys():

            log(str(data[cle]))
            
        #log(str(data.keys()))
        #log(str(data["holdings"]))
        #data_n = data['ohlcv'][0]
        #log(str(data_n['SPY']['open']))
        #for x in data_n:
            #log(x)