import logging
from datetime import datetime, timedelta

from quant_frame.data.symbol import Symbol
from quant_frame.broker.orders import Order


class TradingAlgo:

    _data_callback_function = None
    _order_callback_function = None

    _subscribed_symbols = {}

    def __init__(self, broker, portfolio_manager, time_function):
        # init all modules used
        self.broker = broker
        self.portfolio_manager = portfolio_manager

        # set logger as child logger of package
        self.logger = logging.getLogger(__name__)

        self._time = time_function

    def subscribe_to_symbol(self, symbol: Symbol, resolution: timedelta):
        self.logger.debug(f"Subscribed to {symbol} with a resolution of {resolution}")
        self._subscribed_symbols[symbol] = resolution

    def unsubscribe_from_symbol(self, symbol: Symbol):
        self.logger.debug(f"unsubscribed from symbol {symbol}")
        self._subscribed_symbols.pop(symbol)

    def send_order(self, order: Order):
        self.broker.send_order(order)

    # functions for engine calls

    def _on_data(self, symbol, data):
        if self._data_callback_function is not None:
            try:
                self._data_callback_function(self, symbol, data)
            except TypeError as e:
                self.logger.error(f"data callback function was not correctly registered\n{e}")

    def _on_order(self, order: Order):
        if self._order_callback_function is not None:
            try:
                self._order_callback_function(self, order)
            except TypeError as e:
                self.logger.error(f"order callback function was not correctly registered\n{e}")

    @property
    def time(self):
        return self._time()

    # register callbacks

    def register_order_callback(self, function):
        self._order_callback_function(function)

    def register_data_callback(self, function):
        self._data_callback_function = function
