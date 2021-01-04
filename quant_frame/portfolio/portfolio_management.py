import logging


class PortfolioManager:

    def __init__(self):
        self._cash = 0
        self.logger = logging.getLogger(__name__)

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, value):
        if value < 0:
            self.logger.error("Cash amount should not be less then 0")
            return
        self._cash = value
