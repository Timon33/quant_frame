import logging
import sys

import quant_frame.trading_algo as trading_algo


class MyTradingAlgo(trading_algo.TradingAlgo):
    logger = None

    def __init__(self):
        super().__init__()
        self.data_provider.subscribe_to_equity("SPY", 1200)


def run():
    algo = MyTradingAlgo()
    algo.data_provider.get_equity_quote("SPY")


