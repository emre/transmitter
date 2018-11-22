from .base import BaseAdapter
import requests


class HuobiAdapter(BaseAdapter):

    BASE_URL = "https://api.huobi.pro/market/detail/merged"

    def get_price(self):
        btc_steem_response = requests.get(
            self.BASE_URL, params={"symbol": "steembtc"})
        btc_steem_response_json = self.validate_response(btc_steem_response)

        usd_btc_response = requests.get(
            self.BASE_URL, params={"symbol": "btcusdt"}
        )
        usd_btc_response_json = self.validate_response(usd_btc_response)

        if btc_steem_response_json and usd_btc_response_json:
            btc_steem_pair = btc_steem_response_json["tick"]["close"]
            usd_btc_pair = usd_btc_response_json["tick"]["close"]

            price = round(usd_btc_pair * btc_steem_pair, self.PRICE_PRECISION)
            self.logger.info(self.bundle_adapter_name(f'Price: {price}'))
            return price
