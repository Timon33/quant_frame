import json
import importlib
import logging

from quant_frame.broker.orders import Order


class Broker:

    def __init__(self, config_file):
        config = json.load(config_file)
        self.logger = logging.getLogger(__name__)

        supported_brokers = list(config.keys())[1:]
        self.broker_name = config["broker"]
        self.broker = None

        module_name = config[self.broker_name]["module"]

        if self.broker_name in supported_brokers:
            try:
                self.broker = importlib.import_module("quant_frame.broker." + module_name)
            except ImportError as e:
                logger = logging.getLogger(__name__)
                logger.error(f"The api implementation for {self.api_name} in file {module_name} was not found!\n{e}")
        else:
            raise ValueError(
                f"The requested api {self.api_name} is not supported. Currently supported are {supported_brokers}!")

        self.broker.initialize(config_file)

        # _orders is a dict with symbols as keys containing a list of orders for that symbol
        def send_order(self, order: Order):
            if order.symbol not in self._orders:
                self._orders[order.symbol] = []
            self._orders[order.symbol].append(order)

        def register_order_callback(self, function):
            self._order_callback_function = function

        def on_data(self, symbol, data):
            for order in self._orders[symbol]:
                # check symbol equity type
                pass