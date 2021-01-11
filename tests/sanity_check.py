import logging
import sys
import pandas as pd
from datetime import datetime, timedelta
import sys

sys.path.append(".")

import quant_frame.trading_algo as trading_algo
import quant_frame.engines.back_test_engine as engine
from quant_frame.data.symbol import Symbol
from quant_frame.broker.orders import Order, MarketOrder
from quant_frame.data.data_provider import TimeResolution


class MyTradingAlgo(trading_algo.TradingAlgo):

    def initialize(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("initializing algo")
        self.spy = Symbol("SPY")
        self.subscribe_to_symbol(self.spy, TimeResolution.DAY)

    def on_data(self, symbol, data):
        self.logger.debug(f"\n\n-------------time: {datetime.fromtimestamp(self.time)}-------------------\n")
        # self.logger.info(f"on data symbol: {symbol}, data:\n{data}\n")
        order = MarketOrder(symbol, 1)
        self.broker.send_order(order)


def run():
    formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    backtest = engine.BackTestEngine("config/api_config.json", "config/broker_config.json")
    backtest.back_test(MyTradingAlgo, datetime(year=2020, month=12, day=1), datetime(year=2020, month=12, day=5))


if __name__ == "__main__":
    run()


