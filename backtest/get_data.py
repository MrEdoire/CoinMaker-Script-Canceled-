from settings import *
from api import *
import pandas as pd

class GetData(Settings):

    def __init__(self):
        super(GetData, self).__init__()
        self.client = Client(api_key, api_secret)

        self.fees = float(self.client.get_trade_fee(symbol=self.currency)[0]['takerCommission'])

        # Used for analysis
        self.start_wallet = self.usdt

        self.get_historical_data()

    def get_historical_data(self):
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