from get_data import *
import ta.trend

class Strategy:

    def __init__(self):

        self.import_indicators(high=Data.df['high'], low=Data.df['low'], close=Data.df['close'])

        # Variables to track the performances of the bot
        self.win = 0
        self.loss = 0

        # Is used to prevent the bot from buying when it already bought some crypto
        self.is_buy = False

        # The strategy that we use to buy / sell our currency
        for index, row in Data.df.iterrows():
            if self.is_buy is False and pd.isna(Data.df['EMA 250'][index]) is False:
                # Our conditions to buy
                if Data.df['EMA 250'][index] < Data.df['close'][index] and \
                    Data.df['MACD Line'][index] > Data.df['MACD Signal'][index] and \
                    Data.df['Ichimoku A'][index] >  Data.df['Ichimoku B'][index] and \
                    pd.isna(Data.df['Parabolic SAR Down'][index]) is False:
                    self.buy_currency(index)

            elif self.is_buy is True and Settings.coin > 0:
                # Our conditions to sell.
                if Data.df['close'][index] >= self.buy_price + (self.buy_price * Settings.take_profit):
                    self.sell_currency(index)
                elif Data.df['close'][index] <= self.buy_price - (self.buy_price * Settings.stop_loss):
                    self.sell_currency(index)

    def import_indicators(self, high, low, close):
        # Add all the needed indicators into the Data Frame
        Data.df['EMA 250'] = ta.trend.ema_indicator(close=Data.df['close'], window=250)

        Data.df['Ichimoku A'] = ta.trend.ichimoku_a(high=high, low=low)
        Data.df['Ichimoku B'] = ta.trend.ichimoku_b(high=high, low=low)

        Data.df['Parabolic SAR Down'] = ta.trend.psar_down(high=high, low=low, close=close)

        Data.df['MACD Line'] = ta.trend.macd(close=close)
        Data.df['MACD Signal'] = ta.trend.macd_signal(close=close)

    def buy_currency(self, index):
        self.buy_price = Data.df['close'][index]

        # Update amount to invest
        self.investment = Settings.usdt * Settings.to_invest

        # Make the transaction
        Settings.coin += (self.investment / Data.df['close'][index])
        Settings.coin -= Settings.coin * Data.fees
        Settings.usdt -= self.investment

        self.is_buy = True

        self.return_buy_or_sell(index)

    def sell_currency(self, index):
        self.sell_price = Data.df['close'][index]

        # Make the transaction
        Settings.usdt += Settings.coin * Data.df['close'][index]
        Settings.usdt -= Settings.usdt * Data.fees
        Settings.coin = 0

        self.is_buy = False

        self.return_buy_or_sell(index)

        # Win += 1 if the bot made profit, Loss += if not
        if Data.df['close'][index] > self.buy_price:
            self.win += 1
        else:
            self.loss += 1

    def return_buy_or_sell(self, index):

        print()
        if self.is_buy is True:
            print(f"Buy at {self.buy_price}$ the {Data.df['timestamp'][index]}")
            print(f"fees : {Settings.coin * Data.fees}")
        else:
            print(f"Sell at {self.sell_price}$ the {Data.df['timestamp'][index]}")
            print(f"fees : {Settings.usdt * Data.fees}")
        print()
        print(f"Usdt : {Settings.usdt}")
        print(f"Coin : {Settings.coin}")

Strategy = Strategy()