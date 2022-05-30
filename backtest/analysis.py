from strategy import *
from matplotlib import pyplot as plt

class Analysis(Strategy):

    def __init__(self):
        super().__init__()

        print()
        print(f"Currency : {self.currency}")
        print(f"Interval : {self.interval}")
        print(f"Start wallet : {self.start_wallet}")

        if self.end_period != None:
            print(f"From {self.start_period} to {self.end_period}")
        else:
            print(f"From {self.start_period} to today")

        print("- - - - - - - - - - ")
        print(f"Stop loss % : {self.stop_loss}")
        print(f"Take profit % : {self.take_profit}")

        print("- - - - - - - - - - ")

        print(f"Trades : {self.win + self.loss}")
        print(f"Win : {self.win} ; Loss {self.loss}")
        print(f"Winrate : {(self.win * 100) / (self.win + self.loss)} %")
        print()
        print(f"Profit : {self.usdt}  USDT")
        print(f"Buy & Hold Profit : {((self.start_wallet * self.to_invest) / self.df['close'].iloc[0]) * self.df['close'].iloc[-1]} USDT")

        plt.plot(self.plt_time, self.plt_wallet)
        plt.plot(self.plt_time, self.plt_currency)
        plt.plot(self.plt_time, self.plt_macd_line)
        plt.plot(self.plt_time, self.plt_macd_signal)
        plt.show()

Analysis = Analysis()