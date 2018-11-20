from .base import BaseAdapter
import requests


class BinanceAdapter(BaseAdapter):

    BASE_URL = "https://api.binance.com/api/v3/ticker/price"

    def get_price(self):
        btc_steem_response = requests.get(
            self.BASE_URL, params={"symbol": "STEEMBTC"})
        btc_steem_response_json = self.validate_response(btc_steem_response)

        usd_btc_response = requests.get(
            self.BASE_URL, params={"symbol": "BTCUSDT"}
        )
        usd_btc_response_json = self.validate_response(usd_btc_response)

        if btc_steem_response_json and usd_btc_response_json:
            btc_steem_pair = float(btc_steem_response_json["price"])
            usd_btc_pair = float(usd_btc_response_json["price"])
            price = round(usd_btc_pair * btc_steem_pair, self.PRICE_PRECISION)
            self.logger.info(self.bundle_adapter_name(f'Price: {price}'))
            return price

