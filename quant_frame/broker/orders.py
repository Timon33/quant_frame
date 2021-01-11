from enum import Enum
import datetime
import logging
from typing import Optional

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
    creation_time = None
    filled_price = None

    def __init__(self, symbol: Symbol, quantity: float = None):
        self.logger = logging.getLogger(__name__)
        self.symbol = symbol
        self.quantity = quantity if quantity is not None else symbol.min_quantity
        self.status = OrderStatus.OPEN
        self.creation_time = datetime.datetime.now()

    @property
    def total_filled_price(self) -> Optional[float]:
        if self.filled_price is None:
            logging.warning("can't calculate total filled price before the order has been filled")
            return None
        return self.quantity * self.filled_price

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, value: float):
        if value == 0 or round(value % self.symbol.min_quantity) != 0:
            self.logger.warning(f"can't set the quantity of an order to {value} that has a minimum quantity of {self.symbol.min_quantity}")
        else:
            self._quantity = value

    def __str__(self):
        side = "BUY" if self.quantity > 0 else "SELL"
        return f"{self.status.name}: {side} {self.quantity} {self.symbol.name} @ {self.filled_price}"

    def update(self, status: OrderStatus = None, filled_price: float = None):
        self.status = self.status if status is None else status
        self.filled_price = filled_price if filled_price is not None else None


class MarketOrder(Order):

    def __init__(self, symbol: Symbol, quantity: float = None):
        super().__init__(symbol, quantity)


class LimitOrder(Order):

    limit = None

    def __init__(self, symbol: Symbol, limit: float, quantity: float = None):
        super().__init__(symbol, limit)
        self.limit = limit
