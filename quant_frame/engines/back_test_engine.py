import datetime
import logging
import pandas as pd

import quant_frame.trading_algo as trading_algo
import quant_frame.data.data_provider as data_provider
import quant_frame.broker.backtest_broker as bt_broker
import quant_frame.portfolio.portfolio_management as portfolio_m


class BackTestEngine:

    def __init__(self, api_config_file, broker_config_file):
        self.logger = logging.getLogger(__name__)
        self.api_config_file = api_config_file
        self.broker_config_file = broker_config_file

    def time(self):
        return self.current_time

    def back_test(self, algorithm_class: trading_algo.TradingAlgo, start_time: datetime.datetime, end_time: datetime.datetime):
        self.logger.info(f"starting back test from {start_time} to {end_time}")

        broker = bt_broker.BackTestBroker(self.broker_config_file)
        portfolio = portfolio_m.PortfolioManager()
        algorithm = algorithm_class(broker, portfolio, self.time)
        algorithm.initialize()

        data_p = data_provider.DataProvider(self.api_config_file)
        history_data = {}
        subscribed_symbols = algorithm.subscribed_symbols

        if len(subscribed_symbols) == 0:
            self.logger.warning("the algo is not subscribed to any symbols. wont perform back test")
            return

        for resolution in subscribed_symbols:
            for symbol in subscribed_symbols[resolution]:
                history_data[symbol] = data_p.get_equity_history(symbol, start_time, end_time, resolution)

        self.logger.debug("pulled all history data needed from api")

        time_step_in_seconds = int(sorted(subscribed_symbols)[0].value.total_seconds())
        for self.current_time in range(round(start_time.timestamp()), round(end_time.timestamp()), time_step_in_seconds):
            for resolution in subscribed_symbols:
                # if round((datetime.datetime.fromtimestamp(self.current_time) - start_time) / resolution.value) == 0:
                for symbol in subscribed_symbols[resolution]:
                    algorithm._on_data(symbol, history_data[symbol].loc[pd.Timestamp(start_time): pd.Timestamp(self.current_time + time_step_in_seconds, unit="s")])
