import numpy as np

# from .adapters.binance import BinanceAdapter # disabled temporarily
from .adapters.bittrex import BittrexAdapter
# from .adapters.huobi import HuobiAdapter # disabled temporarily
# from .adapters.upbit import UpbitAdapter # disabled temporarily

AVAILABLE_MARKETS = {
    # "binance": BinanceAdapter,
    "bittrex": BittrexAdapter,  # disabled temporarily
    # "huobi": HuobiAdapter, # disabled temporarily
    # "upbit": UpbitAdapter, # disabled temporarily
}

DEFAULT_MARKETS = list(AVAILABLE_MARKETS.keys())


def is_marketlist_valid(market_list):
    # that's a crazy one liner.
    # it checks the given market list's all elements are defined in implemented
    # markets.
    return len(set(market_list).difference(set(AVAILABLE_MARKETS.keys()))) == 0


def get_prices(markets):
    return [
        AVAILABLE_MARKETS.get(market)().get_price() for market in markets]


def get_average_price(prices):
    return round(sum(prices) / len(prices), 3)


def exclude_outliers(prices, threshold=35):
    """
    An outlier logic to exclude bad markets.
    Uses a slightly modified version of "Modified Z-score".
    https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm
    """
    if isinstance(prices, list):
        prices = np.array(prices)
    original_median = np.median(prices)
    deviation = np.abs(prices - original_median)
    median_deviation = np.median(deviation)
    score = 0
    if median_deviation:
        score = deviation / median_deviation
    filtered_prices = prices[score < threshold]
    return list(filtered_prices)
