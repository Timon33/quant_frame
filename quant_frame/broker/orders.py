from enum import Enum

from quant_frame.data.symbol import Symbol


class OrderStatus(Enum):
    OPEN = 0
    FILLED = 1
    PARTIALLY_FILLED = 2
    CANCELED = 3
    REJECTED = 4
    MARGIN = 5


class Order:

    expiry = None
    status = None
    symbol = None

    def __init__(self):
        pass


class MarketOrder(Order):

    def __init__(self):
        pass


class LimitOrder(Order):

    limit = None

    def __init__(self):
        pass
