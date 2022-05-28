from strategy import *

class Analysis:

    def __init__(self):

        print()
        print(f"Currency : {Settings.currency}")
        print(f"Interval : {Settings.interval}")
        print(f"Start wallet : {Settings.start_wallet}")

        if Settings.end_period != None:
            print(f"From {Settings.start_period} to {Settings.end_period}")
        else:
            print(f"From {Settings.start_period} to today")

        print("- - - - - - - - - - ")
        print(f"Stop loss % : {Settings.stop_loss}")
        print(f"Take profit % : {Settings.take_profit}")

        print("- - - - - - - - - - ")

        print(f"Win : {Strategy.win} ; Loss {Strategy.loss}")
        print(f"Winrate : {(Strategy.win * 100) / (Strategy.win + Strategy.loss)} %")
        print()
        print(f"Profit : {Settings.usdt}  USDT")
        print(f"Buy & Hold Profit : {((Settings.start_wallet * Settings.to_invest) / Data.df['close'].iloc[0]) * Data.df['close'].iloc[-1]} USDT")

Analysis = Analysis()