import logging
import pandas as pd
from collections.abc import Callable

from quant_frame.data.symbol import Symbol
from quant_frame.broker.orders import Order, OrderStatus, MarketOrder, LimitOrder


class BackTestBroker:

    def __init__(self, config_file):
        # read config if needed
        self.logger = logging.getLogger(__name__)
        self.orders = {}

    def send_order(self, order: Order):
        if order.symbol not in self.orders:
            self.orders[order.symbol] = []
        self.orders[order.symbol].append(order)
        self.logger.debug(f"new order: {order}")
        self.logger.debug(f"all orders:")
        for symbol in self.orders:
            self.logger.debug(f"{symbol}: {' - '.join([str(x) for x in self.orders[symbol]])}")

    def set_order_callback_function(self, function):
        self.order_callback_function = function

    def marked_order(self, order: MarketOrder, symbol: Symbol, data: pd.DataFrame):
        order.update(status=OrderStatus.FILLED, filled_price=data.iloc[-1]["close"])
        side = "BUY" if order.quantity > 0 else "SELL"
        self.logger.info(f"filled order: {order}")
        self.order_callback_function(order)

    def limit_order(self, order: LimitOrder, symbol: Symbol, data: pd.DataFrame):
        current_data = data.iloc[-1]
        if order.quantity > 0:
            if order.limit > current_data["low"]:
                order.update(status=OrderStatus.FILLED, filled_price=order.limit)
        elif order.quantity < 0:
            if order.limit < current_data["high"]:
                order.update(status=OrderStatus.FILLED, filled_price=order.limit)
        else:
            logger = logging.getLogger(__name__)
            logger.warning(f"the order to process has a quantity of {order.quantity}. The quantity should not be 0")
            return

        self.logger.info(f"filled order: {order}")
        self.order_callback_function(order)

    def on_data(self, symbol: Symbol, data: pd.DataFrame):
        if symbol not in self.orders:
            return
        print(len(self.orders[symbol]))
        for order in self.orders[symbol]:
            print(order)
            if order.status in [OrderStatus.OPEN, OrderStatus.PARTIALLY_FILLED]:
                # process according to order type
                print(order)
                if type(order) == MarketOrder:
                    self.marked_order(order, symbol, data)
                elif type(order) == LimitOrder:
                    self.limit_order(order, symbol, data)
                else:
                    logger = logging.getLogger(__name__)
                    logger.warning("Order could not be processed, because it is not supported by the used api")

            elif order.status in [OrderStatus.FILLED]:
                self.orders[symbol].remove(order)
