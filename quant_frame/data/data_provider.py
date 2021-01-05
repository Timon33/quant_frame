import logging
import random
import pandas as pd
import numpy as np

import quant_frame.data.data_api as api
from quant_frame.data.symbol import Symbol
from datetime import timedelta, datetime


class DataProvider:
    # used be the respective engine to make callbacks
    _subscribed_symbols = {}

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @property
    def subscribed_symbols(self) -> list:
        return self._subscribed_symbols

    # data_provider handling functions

    def subscribe_to_symbol(self, symbol: Symbol, resolution: timedelta):
        self.logger.debug(f"Subscribed to {symbol} with a resolution of {resolution}")
        self._subscribed_symbols[symbol] = resolution

    def unsubscribe_from_symbol(self, symbol: Symbol):
        self.logger.debug(f"unsubscribed from symbol {symbol}")
        self._subscribed_symbols.pop(symbol)

    def get_equity_quote(self, symbol):
        self.logger.debug(f"getting quote for symbol {symbol}")
        quote = api.get_quote(symbol)
        return quote

    def get_option_expire_dates(self, symbol):
        pass

    def get_option_chain(self, symbol, expiration_date, strikes):
        pass

    def get_equity_history(self, symbol: Symbol, start_time: datetime, end_time: datetime, resolution: timedelta):
        return api.get_historical_data(symbol.name, start_time, end_time, resolution)

    # TODO implement random data
    def get_random_data(self, exp, variance, start_time, end_time, resolution, min_start_price=5.0,max_start_price=1000.0):
        pass
