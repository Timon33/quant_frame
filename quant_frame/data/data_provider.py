import logging
import random
import pandas as pd
import numpy as np

import quant_frame.data.data_api as api


class DataProvider:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    # data_provider handling functions

    def subscribe_to_equity(self, symbol, resolution):
        self.logger.debug(f"Subscribed to {symbol} with a resolution of {resolution}")
        pass

    def get_equity_quote(self, symbol):
        self.logger.debug(f"getting quote for symbol {symbol}")
        quote = api.get_quote(symbol)
        return quote

    def get_option_expire_dates(self, symbol):
        pass

    def get_option_chain(self, symbol, expiration_date, strikes):
        pass

    def get_equity_history(self, symbol, start_time, end_time, resolution):
        pass

    def get_random_data(self, exp, variance, start_time, end_time, resolution, min_start_price=5.0, max_start_price=1000.0):
        price = random.uniform(min_start_price, max_start_price)
        df = pd.DataFrame()
        for t in range(start_time, end_time, resolution):
            delta = np.random.normal(exp, variance)
            price += float(delta)
            df.append({price})

        return df





