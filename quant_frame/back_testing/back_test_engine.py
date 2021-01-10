import datetime
import logging
import pandas as pd

import quant_frame.trading_algo as trading_algo
import quant_frame.data.data_provider as data_provider


class BackTestEngine:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def back_test(self, algorithm: trading_algo.TradingAlgo, start_time: datetime.datetime, end_time: datetime.datetime):
        self.logger.info(f"starting backtest from {start_time} to {end_time}")
        data_p = data_provider.DataProvider()
        history_data = {}
        subscribed_symbols = algorithm.subscribed_symbols

        for resolution in subscribed_symbols:
            for symbol in subscribed_symbols[resolution]:
                history_data[symbol] = data_p.get_equity_history(symbol, start_time, end_time, resolution)
        self.logger.debug("pulled all history data needed from api")

        for current_time in range(round(start_time.timestamp()), round(end_time.timestamp()), sorted(subscribed_symbols)[0]):
            for resolution in subscribed_symbols:
                if round((datetime.datetime.fromtimestamp(current_time) - start_time) / resolution) == 0:
                    for symbol in subscribed_symbols[resolution]:
                        algorithm.on_data(symbol, history_data[symbol].loc[pd.Timestamp(start_time): pd.Timestamp(current_time, unit="s")])




