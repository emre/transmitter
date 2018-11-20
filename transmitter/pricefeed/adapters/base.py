import logging
import requests


class BaseAdapter:

    PRICE_PRECISION = 4

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def get_usd_btc_pair(self):
        resp = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/")
        return float(resp["price_usd"])

    def bundle_adapter_name(self, message):
        return f"{self.__class__.__name__}: {message}"

    def validate_response(self, response):
        if response.status_code != 200:
            self.logger.error(
                self.bundle_adapter_name(
                    f"Invalid HTTP status code: {response.status_code}"))
            return None
        response_json = response.json()
        return response_json

    def get_price(self):
        raise NotImplementedError
