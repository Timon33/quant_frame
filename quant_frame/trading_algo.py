# holds the TradingAlgo class

import logging

import quant_frame.data.data_provider as data_provider
import quant_frame.market.order_management as order_management
import quant_frame.portfolio.portfolio_management as portfolio_management


class TradingAlgo:

    def __init__(self):
        # init all modules used
        self.data_provider = data_provider.DataProvider()
        self.order_manager = order_management.OrderManager()
        self.portfolio_manager = portfolio_management.PortfolioManager()

        # set logger as child of package
        self.logger = logging.getLogger(__name__)

    # callback functions

    def on_market_open(self):
        pass

    def on_market_close(self):
        pass

    def on_data(self, data):
        pass

    def on_fill(self, filled_order):
        pass

    def on_cancel(self, canceled_order):
        pass
