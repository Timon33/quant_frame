import importlib
import logging
import pandas as pd

SUPPORTED_APIS = {"TD Ameritrade": "td_ameritrade_api"}

# for now specified here, should be read from a config or something
api_name = "TD Ameritrade"
api = None

if api_name in SUPPORTED_APIS:
    try:
        api = importlib.import_module("quant_frame.data." + SUPPORTED_APIS[api_name])
    except ImportError as e:
        logger = logging.getLogger(__name__)
        logger.error(f"The api implementation for {api_name} in file {SUPPORTED_APIS[api_name]} was not found!")
else:
    raise ValueError(f"The requested api {api_name} is not supported. Currently supported are {SUPPORTED_APIS}!")


# functions implemented be the apis

def get_quote(*args, **kwargs) -> pd.DataFrame:
    return api.get_quote(*args, **kwargs)


def get_option_expire_dates(*args, **kwargs) -> pd.DataFrame:
    return api.get_option_expire_dates(*args, **kwargs)


def get_option_chain(*args, **kwargs) -> pd.DataFrame:
    return api.get_option_chain(*args, **kwargs)


def get_historical_data(*args, **kwargs) -> pd.DataFrame:
    return api.get_historical_data(*args, **kwargs)