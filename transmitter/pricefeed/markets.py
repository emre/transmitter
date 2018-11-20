from .adapters.binance import BinanceAdapter
from .adapters.poloniex import PoloniexAdapter
from .adapters.bittrex import BittrexAdapter

AVAILABLE_MARKETS = {
    "poloniex": PoloniexAdapter,
    "binance": BinanceAdapter,
    "bittrex": BittrexAdapter,
}


def is_marketlist_valid(market_list):
    # that's a crazy one liner.
    # it checks the given market list's all elements are defined in implemented
    # markets.
    return len(set(market_list).difference(set(AVAILABLE_MARKETS.keys()))) == 0


def get_average_price(markets):
    prices = [
        AVAILABLE_MARKETS.get(market)().get_price() for market in markets]
    return round(sum(prices) / len(prices), 3)


