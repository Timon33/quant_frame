import logging

from quant_frame.broker.orders import Order


class Broker:

    # used for callbacks
    _orders = {}

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def send_order(self, order: Order):
        if not order.symbol in self._orders:
            self._orders[order.symbol] = []
        self._orders[order.symbol].append(order)

    def register_order_callback(self, function):
        self._order_callback_function = function

    def on_data(self, symbol, data):
        pass



