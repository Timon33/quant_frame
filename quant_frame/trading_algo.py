import logging
import pandas as pd

from quant_frame.data.symbol import Symbol
from quant_frame.broker.orders import Order
from quant_frame.data.data_provider import TimeResolution


class TradingAlgo:

    _data_callback_function = None
    _order_callback_function = None

    _subscribed_symbols = {}

    def __init__(self, broker, portfolio_manager, time_function):
        # init all modules used
        self.broker = broker
        self.broker.set_order_callback_function(self.on_order)
        self.portfolio_manager = portfolio_manager

        # set logger as child logger of package
        self.logger = logging.getLogger(__name__)

        self._time = time_function

    def subscribe_to_symbol(self, symbol: Symbol, resolution: TimeResolution):
        self.logger.debug(f"Subscribed to {symbol} with a resolution of {resolution}")
        if resolution not in self._subscribed_symbols:
            self._subscribed_symbols[resolution] = []
        self._subscribed_symbols[resolution].append(symbol)

    def unsubscribe_from_symbol(self, symbol: Symbol, resolution: TimeResolution):
        self.logger.debug(f"unsubscribed from symbol {symbol}")
        self._subscribed_symbols.pop(symbol)

    @property
    def subscribed_symbols(self):
        return self._subscribed_symbols

    def send_order(self, order: Order):
        self.broker.send_order(order)

    # functions for engine calls

    def _on_data(self, symbol, data):
        try:
            self.on_data(symbol, data)
        except TypeError as e:
            self.logger.error(f"on_data function was not overwritten correctly\n{e}")
        self.logger.debug(f"calling broker.on_data")
        self.broker.on_data(symbol, data)

    def _on_order(self, order: Order):
        try:
            self.on_order(self, order)
        except TypeError as e:
            self.logger.error(f"on_order function was not overwritten correctly\n{e}")

    @property
    def time(self):
        return self._time()

    # callbacks

    def initialize(self):
        pass

    def on_data(self, symbol: Symbol, data: pd.DataFrame):
        pass

    def on_order(self, order: Order):
        pass
