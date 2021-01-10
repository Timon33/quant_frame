import logging

from quant_frame.broker.orders import Order


def initialize(self, config_file):
    # read config if needed
    self.logger = logging.getLogger(__name__)


