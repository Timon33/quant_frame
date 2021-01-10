import logging
import requests
import json
import pandas as pd
import datetime

API_KEY = ""
API_ENDPOINT = ""
USE_OAUTH = ""


def initialize(config_file):
    global API_KEY, API_ENDPOINT, USE_OAUTH

    logger = logging.getLogger(__name__)

    config = json.load(config_file)
    if config["api"] != "TD Ameritrade":
        logging.error("The api specified was not TD Ameritrade, but it was loaded anyways")

    try:
        api_config = config["TD Ameritrade"]
        API_KEY = api_config["api_key"]
        API_ENDPOINT = api_config["api_endpoint"]
        USE_OAUTH = api_config["use_oauth"] == "true"
    except KeyError as e:
        logger.error(f"api config file is corrupted and does not contain all needed configuration")
        exit(1)


# TODO implement oauth2
def make_authenticated_request(endpoint, data, params):
    return None


def make_unauthenticated_request(endpoint, data, params):
    params["apikey"] = API_KEY
    logger = logging.getLogger(__name__)
    logger.debug(f"sending request:\ndata: {data}\nparams: {params}")
    response = requests.get(endpoint, data=data, params=params)

    if response.status_code != 200:
        logger.error(f"API Error\nStatus code: {response.status_code}\nResponse:\n{response.text}")
        return None

    return response


def make_request(endpoint: str, data=None, params=None) -> pd.DataFrame:
    data = {} if data is None else data
    params = {} if params is None else params

    logger = logging.getLogger(__name__)

    # use oauth or just the api key for the request
    if USE_OAUTH:
        response = make_authenticated_request(endpoint, data=data, params=params)
    else:
        response = make_unauthenticated_request(endpoint, data=data, params=params)

    # convert to pandas dataframe
    try:
        json_response = json.loads(response.text)
        df = pd.DataFrame.from_dict(json_response)
    except Exception as exp:
        logger.error(f"API response could not be passed correctly to pandas dataframe.\n{exp}")
        return pd.DataFrame()

    return df


def get_quote(symbol):
    logger = logging.getLogger(__name__)
    logger.debug(f"getting quote for {symbol}")
    response = make_request(API_ENDPOINT + f"marketdata/{symbol}/quotes")
    return response


def get_option_expire_dates(symbol: str) -> list:
    logger = logging.getLogger(__name__)
    logger.debug(f"getting option expire dates for {symbol}")
    query_params = {"symbol": symbol, "strikeCount": 1}
    response = make_request(API_ENDPOINT + "marketdata/chains", params=query_params)
    response = response["daysToExpiration"].index.to_list()
    response = [x.split(":")[0] for x in response]
    return response


def get_option_chain(symbol, expiration_date, strikes):
    pass


# turn a timedelta into frequency type and frequency for use by td api
# TODO use nearest frequency pair if timedelta is not exactly supported
def timedelta_to_frequency(timedelta: datetime.timedelta) -> (str, int):
    accepted_combinatons = {
        "minute": [1, 5, 10, 15, 30],
        "daily": [1],
        "weekly": [1],
        "monthly": [1]
    }

    timedeltas = {
        "minute": datetime.timedelta(minutes=1),
        "daily": datetime.timedelta(days=1),
        "weekly": datetime.timedelta(weeks=1),
        "monthly": datetime.timedelta(days=30)
    }

    logger = logging.getLogger(__name__)

    for frequency_type in accepted_combinatons:
        frequency = int(timedelta / timedeltas[frequency_type])
        if frequency in accepted_combinatons[frequency_type]:
            return frequency_type, frequency

    logger.error("Time resulution can not be used by TD Ameritrade API, using daily resulution instead. See https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory")

    return "daily", 1


def get_historical_data(symbol, start_time: datetime.datetime, end_time: datetime.datetime,
                        resolution: datetime.timedelta):
    logger = logging.getLogger(__name__)

    endpoint = API_ENDPOINT + "marketdata/{}/pricehistory".format(symbol)
    frequency_type, frequency = timedelta_to_frequency(resolution)
    period_type = "day" if frequency_type == "minute" else "year"  # adjust the period type so it works for the frequency

    params = {"symbol": symbol,
              "startDate": int(start_time.timestamp() * 1000),  # convert to epoch time in ms
              "endDate": int(end_time.timestamp() * 1000),
              "periodType": period_type,
              "frequencyType": frequency_type,
              "frequency": frequency}

    logger.debug(f"getting historical data for {symbol}")
    df = make_request(endpoint, params=params)
    df = df.candles.apply(pd.Series)  # unpack the candles column
    df.set_index("datetime", inplace=True)
    df.index = df.index.map(lambda x: datetime.datetime.fromtimestamp(x / 1000))  # convert epoch ms to datetime
    return df
