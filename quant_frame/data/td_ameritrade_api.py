import logging
import requests
import json
import pandas as pd

API_ENDPOINT = "https://api.tdameritrade.com/v1/"

# TODO
API_KEY = "8WT8Q3OTCHALL7NYJLLMWXOFYZG3W2JS"
AUTH_KEY = ""

USE_AUTH = False

logger = logging.getLogger(__name__)


# TODO
def make_authenticated_request(endpoint, data, params):
    pass


def make_unauthenticated_request(endpoint, data, params):
    params["apikey"] = API_KEY
    logger.debug(f"sending request:\ndata: {data}\nparams: {params}")
    response = requests.get(endpoint, data=data, params=params)

    if response.status_code != 200:
        logger.error(f"API Error\nStatus code: {response.status_code}\nResponse:\n{response.text}")
        return

    return response


def make_request(endpoint: str, data=None, params=None) -> pd.DataFrame:
    data = {} if data is None else data
    params = {} if params is None else params

    # use oauth or just the api key for the request
    if USE_AUTH:
        response = make_authenticated_request(endpoint, data=data, params=params)
    else:
        response = make_unauthenticated_request(endpoint, data=data, params=params)

    # convert to pandas dataframe
    try:
        json_response = json.loads(response.text)
        df = pd.DataFrame.from_dict(json_response)
    except Exception as e:
        logger.error(f"API response could not be passed correctly to pandas dataframe.\n{e}")
        return

    return df


def get_quote(symbol):
    logger.debug(f"getting quote for {symbol}")
    response = make_request(API_ENDPOINT + f"marketdata/{symbol}/quotes")
    return response


def get_option_expire_dates(symbol: str) -> list:
    logger.debug(f"getting option expire dates for {symbol}")
    query_params = {"symbol": symbol, "strikeCount": 1}
    response = make_request(API_ENDPOINT + "marketdata/chains", params=query_params)
    response = response["daysToExpiration"].index.to_list()
    response = [x.split(":")[0] for x in response]
    return response


def get_option_chain(symbol, expiration_date, strikes):
    pass


def get_historical_data(symbol, from_date, to_date, frequency_type, frequency):
    endpoint = API_ENDPOINT + "marketdata/{}/pricehistory".format(symbol)
    params = {"symbol": symbol,
              "startDate": str(int(from_date * 1000)),  # convert to epoch time in ms
              "endDate": str(int(to_date * 1000)),
              "frequencyType": frequency_type,
              "frequency": frequency}
    return make_request(endpoint, params=params)


def get_historical_data(symbol, period_type, period, frequency_type, frequency):
    endpoint = API_ENDPOINT + "marketdata/{}/pricehistory".format(symbol)
    params = {"symbol": symbol,
              "periodType": period_type,
              "period": period,
              "frequencyType": frequency_type,
              "frequency": frequency}
    return make_request(endpoint, params=params)
