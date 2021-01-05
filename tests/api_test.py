import logging
import datetime

import quant_frame.data.data_api as api
import quant_frame.data.data_provider as provider


def run():
    logger = logging.getLogger(__name__)

    p = provider.DataProvider()
    print(p.get_equity_history("SPY", datetime.datetime(year=2020, month=1, day=1),
                                     datetime.datetime(year=2021, month=1, day=1), datetime.timedelta(days=1)))
