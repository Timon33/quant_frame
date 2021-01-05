# holds the TradingAlgo class

import logging

import quant_frame.data.data_provider as data_provider
import quant_frame.broker.broker as broker
import quant_frame.portfolio.portfolio_management as portfolio_management


class TradingAlgo:

    def __init__(self):
        # init all modules used
        self.data_provider = data_provider.DataProvider()
        self.broker = broker.Broker()
        self.portfolio_manager = portfolio_management.PortfolioManager()

        # set logger as child of package
        self.logger = logging.getLogger(__name__)

    # callback functions

    def on_market_open(self):
        pass

    def on_market_close(self):
        pass

    def _on_data(self, symbol, data):
        self.on_data(self, symbol, data)
        self.broker.on_data(symbol, data)

    def on_data(self, symbol, data):
        pass

    def on_fill(self, filled_order):
        pass

    def on_cancel(self, canceled_order):
        pass

    # register callbacks

    def register_order_callback(self, function):
        self.broker.register_order_callback(function)
