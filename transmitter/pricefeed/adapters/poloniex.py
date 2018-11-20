from .base import BaseAdapter
import requests


class PoloniexAdapter(BaseAdapter):

    def get_price(self):
        ticker_data = requests.get(
            "https://poloniex.com/public?command=returnTicker")

        ticker_data = self.validate_response(ticker_data)
        if ticker_data:
            usdt_btc_pair = float(ticker_data["USDT_BTC"]["last"])
            btc_steem_pair = float(ticker_data["BTC_STEEM"]["last"])
            price = round(usdt_btc_pair * btc_steem_pair, self.PRICE_PRECISION)
            self.logger.info(self.bundle_adapter_name(f'Price: {price}'))
            return price
