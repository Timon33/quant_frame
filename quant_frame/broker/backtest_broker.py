import logging
import pandas as pd
from collections.abc import Callable

from quant_frame.data.symbol import Symbol
from quant_frame.broker.orders import Order, OrderStatus, MarketOrder, LimitOrder

ORDERS = {}
ORDER_CALLBACK = None


def initialize(self, config_file):
    # read config if needed
    pass


def send_order(order: Order):
    if order.symbol not in ORDERS:
        ORDERS[order.symbol] = []
    ORDERS[order.symbol].append(order)


def set_order_callback_function(function: Callable[[Order], None]):
    global ORDER_CALLBACK
    ORDER_CALLBACK = function


def marked_order(order: MarketOrder, symbol: Symbol, data: pd.DataFrame):
    order.update(status=OrderStatus.FILLED, filled_price=data.iloc[-1]["close"])
    ORDER_CALLBACK(order)


def limit_order(order: LimitOrder, symbol: Symbol, data: pd.DataFrame):
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

    ORDER_CALLBACK(order)


def on_data(symbol: Symbol, data: pd.DataFrame):
    for order in ORDERS[symbol]:
        if order.status in [OrderStatus.OPEN, OrderStatus.PARTIALLY_FILLED]:
            # process according to order type
            if type(order) == MarketOrder:
                marked_order(order, symbol, data)
            elif type(order) == LimitOrder:
                limit_order(order, symbol, data)
            else:
                logger = logging.getLogger(__name__)
                logger.warning("Order could not be processed, because it is not supported by the used api")
