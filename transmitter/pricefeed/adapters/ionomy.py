from .base import BaseAdapter
import requests


class IonomyAdapter(BaseAdapter):

    BASE_URL = "https://ionomy.com/api/v1/public/orderbook"

    def get_price(self):
        btc_hive_response = requests.get(
            self.BASE_URL,
            params={"market": "btc-hive", "type": "asks"})

        btc_hive_response_json = self.validate_response(btc_hive_response)

        usd_btc_response =requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids="
            "bitcoin&vs_currencies=usd"
        )
        usd_btc_response_json = self.validate_response(usd_btc_response)

        if btc_hive_response_json and usd_btc_response_json:
            btc_hive_pair = btc_hive_response_json["data"]["asks"][0]["price"]
            usd_btc_pair = usd_btc_response_json["bitcoin"]["usd"]

            price = round(usd_btc_pair * float(btc_hive_pair), self.PRICE_PRECISION)
            self.logger.info(self.bundle_adapter_name(f'Price: {price}'))
            return price
