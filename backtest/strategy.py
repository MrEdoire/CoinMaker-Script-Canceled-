from get_data import *
import ta.trend

class Strategy(GetData):

    def __init__(self):
        super().__init__()
        self.import_indicators(high=self.df['high'], low=self.df['low'], close=self.df['close'])

        # Variables to track the performances of the bot
        self.win = 0
        self.loss = 0

        # Used for charts
        self.plt_time = []
        self.plt_wallet = []
        self.plt_currency = []
        self.plt_macd_line = []
        self.plt_macd_signal = []

        # Is used to prevent the bot from buying when it already bought some crypto
        self.is_buy = False

        # The strategy that we use to buy / sell our currency
        for index, row in self.df.iterrows():

            if self.is_buy is False and pd.isna(self.df['EMA 100'][index]) is False:
                # Our conditions to buy
                if self.df['EMA 100'][index] < self.df['close'][index] and \
                    self.df['MACD Line'][index] > self.df['MACD Signal'][index]:
                    self.buy_currency(index)

            elif self.is_buy is True and self.coin > 0:
                # Our conditions to sell.
                if self.df['close'][index] >= self.buy_price + (self.buy_price * self.take_profit):
                    self.sell_currency(index)
                elif self.df['close'][index] <= self.buy_price - (self.buy_price * self.stop_loss):
                    self.sell_currency(index)

    def import_indicators(self, high, low, close):
        # Add all the needed indicators into the Data Frame
        self.df['EMA 100'] = ta.trend.ema_indicator(close=close, window=100)

        self.df['Ichimoku A'] = ta.trend.ichimoku_a(high=high, low=low)
        self.df['Ichimoku B'] = ta.trend.ichimoku_b(high=high, low=low)

        self.df['Parabolic SAR Down'] = ta.trend.psar_down(high=high, low=low, close=close)

        self.df['MACD Line'] = ta.trend.macd(close=close)
        self.df['MACD Signal'] = ta.trend.macd_signal(close=close)

    def buy_currency(self, index):
        self.buy_price = self.df['close'][index]

        # Update amount to invest
        self.investment = self.usdt * self.to_invest

        # Make the transaction
        self.coin += self.investment / self.df['close'][index]
        self.coin -= (self.investment / self.df['close'][index]) * self.fees
        self.usdt -= self.investment

        self.is_buy = True

        self.return_buy_or_sell(index)

    def sell_currency(self, index):
        self.sell_price = self.df['close'][index]

        # Make the transaction
        self.usdt += self.coin * self.df['close'][index]
        self.usdt -= (self.coin * self.df['close'][index]) * self.fees
        self.coin = 0

        self.plt_time.append(self.df['timestamp'][index])
        self.plt_wallet.append(self.usdt)
        self.plt_currency.append(self.df['close'][index])
        self.plt_macd_line.append(self.df['MACD Line'][index])
        self.plt_macd_signal.append(self.df['MACD Signal'][index])

        self.is_buy = False

        self.return_buy_or_sell(index)

        # Win += 1 if the bot made profit, Loss += if not
        if self.df['close'][index] > self.buy_price:
            self.win += 1
        else:
            self.loss += 1

    def return_buy_or_sell(self, index):

        print()
        if self.is_buy is True:
            print(f"Buy at {self.buy_price}$ the {self.df['timestamp'][index]}")
            print(f"fees : {self.coin * self.fees}")
        else:
            print(f"Sell at {self.sell_price}$ the {self.df['timestamp'][index]}")
            print(f"fees : {self.usdt * self.fees}")
        print()
        print(f"Usdt : {self.usdt}")
        print(f"Coin : {self.coin}")
