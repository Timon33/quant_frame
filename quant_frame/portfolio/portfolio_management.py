import logging

from quant_frame.broker.orders import Order, OrderStatus


class PortfolioManager:

    def __init__(self):
        self._cash = 0
        self.logger = logging.getLogger(__name__)
        self.positions = {}

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, value):
        if value < 0:
            self.logger.error("Cash amount should not be less then 0")
            return
        self._cash = value

    def process_order(self, order: Order):
        if order.status == OrderStatus.FILLED:
            self.cash -= order.total_filled_price
            self.positions[order.symbol] = order.quantity

