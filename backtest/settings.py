from binance import Client

class Settings:

    def __init__(self):

        self.currency = 'ETHUSDT'
        self.interval = Client.KLINE_INTERVAL_4HOUR
        self.start_period = '01 January 2021'
        self.end_period = None

        self.usdt = 500
        self.coin = 0
        self.stop_loss = 0.05
        self.take_profit = 0.15
        self.to_invest = 1   # % of the wallet to invest (1 = 100%)

        self.reload_currency_data = False
