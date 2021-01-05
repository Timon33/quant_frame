import logging


class TradingAlgo:

    def __init__(self, data_provider, broker, portfolio_manager, time_function):
        # init all modules used
        self.data_provider = data_provider
        self.broker = broker
        self.portfolio_manager = portfolio_manager

        # set logger as child logger of package
        self.logger = logging.getLogger(__name__)

        self._time = time_function

    # functions for engine calls

    def _on_data(self, symbol, data):
        if self._data_callback_function is not None:
            try:
                self._data_callback_function(self, symbol, data)
            except TypeError as e:
                self.logger.error(f"data callback function was not correctly registered\n{e}")

    # functions implemented by the engine

    @property
    def time(self):
        return self._time()

    # register callbacks

    def register_order_callback(self, function):
        self.broker.register_order_callback(function)

    def register_data_callback(self, function):
        self._data_callback_function = function
