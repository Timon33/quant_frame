import logging
import importlib
import json

from quant_frame.data.symbol import Symbol
from datetime import timedelta, datetime


class DataProvider:

    def __init__(self, config_file):
        self.logger = logging.getLogger(__name__)

        config = json.load(config_file)

        supported_apis = list(config.keys())[1:]

        # TODO for now specified here, should be read from a config or something
        self.api_name = "TD Ameritrade"
        self.api = None

        module_name = config[self.api_name]["module"]

        if self.api_name in supported_apis:
            try:
                self.api = importlib.import_module("quant_frame.data." + module_name)
            except ImportError as e:
                logger = logging.getLogger(__name__)
                logger.error(f"The api implementation for {self.api_name} in file {module_name} was not found!\n{e}")
        else:
            raise ValueError(
                f"The requested api {self.api_name} is not supported. Currently supported are {supported_apis}!")

        self.api.inititalize(config_file)

    # data_provider handling functions

    def get_equity_quote(self, symbol):
        self.logger.debug(f"getting quote for symbol {symbol}")
        quote = self.api.get_quote(symbol)
        return quote

    def get_option_expire_dates(self, symbol):
        pass

    def get_option_chain(self, symbol, expiration_date, strikes):
        pass

    def get_equity_history(self, symbol: Symbol, start_time: datetime, end_time: datetime, resolution: timedelta):
        return self.api.get_historical_data(symbol.name, start_time, end_time, resolution)

    # TODO implement random data
    def get_random_data(self, exp, variance, start_time, end_time, resolution, min_start_price=5.0, max_start_price=1000.0):
        pass
