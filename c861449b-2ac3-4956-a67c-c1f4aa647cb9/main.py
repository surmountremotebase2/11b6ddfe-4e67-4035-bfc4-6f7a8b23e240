from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership, InsiderTrading

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["SPY", "QQQ", "AAPL", "GOOGL"]
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
        allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
        for i in self.data_list:
            if tuple(i)[0]=="insider_trading":
                if data[tuple(i)] and len(data[tuple(i)])>0:
                    if "Sale" in data[tuple(i)][-1]['transactionType']:
                        allocation_dict[tuple(i)[1]] = 0

        return TargetAllocation(allocation_dict)
This is an interesting strategy that buys QQQ midday if there is a V shape in the last 3 candles:

from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["QQQ"]

    @property
    def interval(self):
        return "1hour"

    def run(self, data):
        d = data["ohlcv"]
        qqq_stake = 0
        if len(d)>3 and "13:00" in d[-1]["QQQ"]["date"]:
            v_shape = d[-2]["QQQ"]["close"]<d[-3]["QQQ"]["close"] and d[-1]["QQQ"]["close"]>d[-2]["QQQ"]["close"]
            log(str(v_shape))
            if v_shape:
                qqq_stake = 1

        return TargetAllocation({"QQQ": qqq_stake})