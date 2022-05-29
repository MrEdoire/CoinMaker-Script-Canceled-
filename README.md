
# CoinMaker

An easy-to-use Bot that trades crypto using [Binance's](https://www.binance.com/en) API.

### How to install the requirements ?
```
pip install -r requirements.txt
```
## Upcoming features :
- A fully working backtest program with data analysis
- The bot itself that could make trades on Binance 24/7
- A complete tracking of the bot's performances over time

## Backtest basic settings

When you open the [settings.py](backtest/settings.py), use the following variables to setup your backtest :

```python
self.currency = 'ETHUSDT'
self.interval = Client.KLINE_INTERVAL_1HOUR
self.start_period = '01 January 2021'
self.end_period = None

self.usdt = 500
self.coin = 0
self.stop_loss = 0.10
self.take_profit = 0.15
self.to_invest = 1   # % of the wallet to invest (1 = 100%)

self.reload_currency_data = False
```

Make sure to set `self.reload_currency_data` as `True` everytime you change something. It will
get the data of your currency with the modified settings and return them in the [data.csv](backtest/data.csv) file. Then, you
can  set the variable to `False` as the program will use the csv file to process.

## Known issue

When you launch the [settings.py](backtest/settings.py) file, it is possible that you get the following error :

```
FutureWarning: The default dtype for empty Series will be 'object' instead of 'float64' in a future version. Specify a dtype explicitly to silence this warning.
  self._psar_up = pd.Series(index=self._psar.index)
  
FutureWarning: The default dtype for empty Series will be 'object' instead of 'float64' in a future version. Specify a dtype explicitly to silence this warning.
  self._psar_down = pd.Series(index=self._psar.index)
```
To fix it, you need to go to the trend.py file of your `ta` package and find the following 
function (line 931):

```python
def _run(self):  # noqa
    up_trend = True
    acceleration_factor = self._step
    up_trend_high = self._high.iloc[0]
    down_trend_low = self._low.iloc[0]

    self._psar = self._close.copy()
    self._psar_up = pd.Series(index=self._psar.index)
    self._psar_down = pd.Series(index=self._psar.index)
```

Then, you simply have to add `dtype='object'` in the parameters of the `self._psar_up` and
`self._psar_down` variables :

```python
self._psar_up = pd.Series(index=self._psar.index, dtype='object')
self._psar_down = pd.Series(index=self._psar.index, dtype='object')
```
After that, the error should stop appearing.
