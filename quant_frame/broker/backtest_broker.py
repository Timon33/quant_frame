import logging

from quant_frame.broker.orders import Order


class Broker:

    _orders = {}

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    # for back-testing the order will be executed when there is new data
    def send_order(self, order: Order):
        if not order.symbol in self._orders:
            self._orders[order.symbol] = []
        self._orders[order.symbol].append(order)

    def register_order_callback(self, function):
        self._order_callback_function = function

    def on_data(self, symbol, data):
        for order in self._orders[symbol]:
            # check symbol equity type
            pass
