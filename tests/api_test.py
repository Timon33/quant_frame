import logging

import quant_frame.data.data_api as api
import quant_frame.data.data_provider as provider

def run():
    logger = logging.getLogger(__name__)

    p = provider.DataProvider()
    logger.info(p.get_random_data(0, 3, 0, 10000, 10))