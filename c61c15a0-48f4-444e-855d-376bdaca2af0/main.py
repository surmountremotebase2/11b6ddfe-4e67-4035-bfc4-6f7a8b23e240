from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.technical_indicators import SMA, ATR
import matplotlib.pyplot as plt

class ResistanceStrategy(Strategy):
    def __init__(self, asset: Asset, window: int = 14, atr_multiplier: float = 2):
        super().__init__()
        self.asset = asset
        self.window = window
        self.atr_multiplier = atr_multiplier
        self.sma = SMA(asset, window)
        self.atr = ATR(asset, window)
        self.positions = []

    def identify_resistance(self):
        data = self.asset.get_data()
        resistance_levels = []
        for i in range(self.window, len(data)):
            high = data['High'][i-self.window:i+1].max()
            if data['Close'][i] >= high:
                resistance_levels.append((data.index[i], high))
        return resistance_levels

    def execute_strategy(self):
        data = self.asset.get_data()
        resistance_levels = self.identify_resistance()

        buy_price = None
        sell_price = None

        for i in range(len(data)):
            if buy_price is None:
                buy_price = data['Close'][i]

            for level in resistance_levels:
                if data.index[i] >= level[0] and data['Close'][i] >= level[1]:
                    sell_price = data['Close'][i]
                    self.positions.append((buy_price, sell_price))
                    buy_price = None
                    break

    def plot_results(self):
        data = self.asset.get_data()
        resistance_levels = self.identify_resistance()

        plt.figure(figsize=(14, 7))
        plt.plot(data['Close'], label='Close Price')

        for level in resistance_levels:
            plt.axhline(y=level[1], color='r', linestyle='--', lw=0.5)
            plt.text(level[0], level[1], 'Resistance', color='r')

        plt.title(f'{self.asset.symbol} Stock Price and Resistance Levels')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

    def print_positions(self):
        for position in self.positions:
            print(f'Bought at: {position[0]}, Sold at: {position[1]}')


asset = Asset('AAPL', '2023-01-01', '2023-12-31')
strategy = ResistanceStrategy(asset)
strategy.execute_strategy()
strategy.plot_results()
strategy.print_positions()


This example provides a basic framework and can be expanded with more sophisticated logic and risk management techniques.