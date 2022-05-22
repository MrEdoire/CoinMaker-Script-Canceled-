import ta.trend
from binance import Client
import pandas as pd
from matplotlib import pyplot as plt
from api import *

class Backtest:

    def __init__(self):

        self.client = Client(api_key, api_secret)

        # - - - - SETTINGS - - - - -
        self.currency = 'ETHUSDT'
        self.interval = Client.KLINE_INTERVAL_1HOUR
        self.start_period = '01 January 2021'
        self.end_period = None

        self.fees = float(self.client.get_trade_fee(symbol=self.currency)[0]['takerCommission'])

        self.usdt = 500
        self.coin = 0
        self.stop_loss = 0.05
        self.take_profit = 0.15
        self.to_invest = self.usdt * 0.1   # % of the wallet to invest

        self.reload_currency_data = False   # Need to be True to apply any changes in settings

        # Used for analysis
        self.start_wallet = self.usdt

        # - - - - - - - - - - - - - -

        self.get_historical_datas()
        self.strategy()
        self.analysis()

    def get_historical_datas(self):
        # Get a dataframe from the chosen currency
        if self.reload_currency_data is True:
            # Get from the Binance API all the historical data of the chosen currency
            self.create_data_frame(Client().get_historical_klines(self.currency, self.interval,
                                                                  self.start_period, self.end_period))
            self.df.to_csv('data.csv')
        else:
            # Use the data.csv to get the data of the chosen currency
            self.create_data_frame(pd.read_csv('data.csv'))

        # Converting timestamps into dates
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], unit='ms')

    def create_data_frame(self, source):
        # Create a Data Frame out of our source (klinesT or csv file)
        self.df = pd.DataFrame(source, columns=['timestamp', 'open', 'high',
                                                'low', 'close', 'volume',
                                                'close_time', 'quote_av', 'trades',
                                                'tb_base_av', 'tb_quote_av', 'ignore'])
        # Deleting columns that are useless
        self.to_delete = ['ignore', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av']
        for i in self.to_delete:
            del self.df[i]

        # Converting the used columns to numeric
        self.to_numeric = ['close', 'high', 'low', 'open']
        for i in self.to_numeric:
            self.df[i] = pd.to_numeric(self.df[i])

    def strategy(self):
        # Import the indicators to apply the strategy
        self.import_indicators(high=self.df['high'], low=self.df['low'], close=self.df['close'])

        # Variables to track the performances of the bot
        self.win = 0
        self.loss = 0

        # Is used to prevent the bot from buying when it already bought some crypto
        self.is_buy = False

        # The strategy that we use to buy / sell our currency
        for index, row in self.df.iterrows():
            if self.is_buy is False and pd.isna(self.df['EMA 250'][index]) is False:
                # Our conditions to buy
                if self.df['EMA 250'][index] < self.df['close'][index] and \
                    self.df['MACD Line'][index] > self.df['MACD Signal'][index] and \
                    self.df['Ichimoku A'][index] >  self.df['Ichimoku B'][index] and \
                    pd.isna(self.df['Parabolic SAR Down'][index]) is False:
                    self.buy_currency(index)

            elif self.is_buy is True and self.coin > 0:
                # Our conditions to sell.
                if self.df['close'][index] >= self.buy_price + (self.buy_price * self.take_profit):
                    self.sell_currency(index)
                elif self.df['close'][index] <= self.buy_price - (self.buy_price * self.stop_loss):
                    self.sell_currency(index)

    def import_indicators(self, high, low, close):
        # Add all the needed indicators into the Data Frame
        self.df['EMA 250'] = ta.trend.ema_indicator(close=self.df['close'], window=250)

        self.df['Ichimoku A'] = ta.trend.ichimoku_a(high=high, low=low)
        self.df['Ichimoku B'] = ta.trend.ichimoku_b(high=high, low=low)

        self.df['Parabolic SAR Down'] = ta.trend.psar_down(high=high, low=low, close=close)

        self.df['MACD Line'] = ta.trend.macd(close=close)
        self.df['MACD Signal'] = ta.trend.macd_signal(close=close)

    def buy_currency(self, index):
        self.buy_price = self.df['close'][index]

        self.coin += (self.to_invest / self.df['close'][index])
        self.coin -= self.coin * self.fees
        self.usdt -= self.to_invest

        self.is_buy = True

        self.return_buy_or_sell(index)

    def sell_currency(self, index):
        self.sell_price = self.df['close'][index]

        self.usdt += self.coin * self.df['close'][index]
        self.usdt -= self.usdt * self.fees
        self.coin = 0

        self.is_buy = False

        self.return_buy_or_sell(index)

        # Win += 1 if the bot made profit, Loss += if not
        if self.df['close'][index] > self.buy_price:
            self.win += 1
        else:
            self.loss += 1

    def return_buy_or_sell(self, index):

        if self.is_buy is True:
            print(f"Buy at {self.buy_price}$ the {self.df['timestamp'][index]}")
            print(f"fees : {self.coin * self.fees}")
        else:
            print(f"Sell at {self.sell_price}$ the {self.df['timestamp'][index]}")
            print(f"fees : {self.usdt * self.fees}")
        print(self.usdt)
        print(self.coin)

    def analysis(self):

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

        print(f"Win : {self.win} ; Loss {self.loss}")
        print(f"Winrate : {(self.win * 100) / (self.win + self.loss)} %")
        print()
        print(f"Profit : {self.usdt}  USDT")
        print(f"Buy & Hold Profit : {(self.to_invest / self.df['close'].iloc[0]) * self.df['close'].iloc[-1]} USDT")


backtest = Backtest()

def chart():
    indicators_list = ['close', 'EMA 250', 'MACD Line', 'MACD Signal',
                       'Parabolic SAR Down', 'Ichimoku A', 'Ichimoku B']
    for i in indicators_list:
        plt.plot(backtest.df['timestamp'], backtest.df[i])
    plt.show()

