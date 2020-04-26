from .base import BaseAdapter
import requests


class MxcAdapter(BaseAdapter):
    BASE_URL = "https://www.mxc.com/open/api/v2/market/ticker"

    def get_price(self):

        if not self.config.get("MXC_API_KEY"):
            raise ValueError(
                "You need to provide MXC_API_KEY environment variable.")

        hive_usdt_response = requests.get(
            self.BASE_URL,
            params={"api_key": self.config["MXC_API_KEY"], "symbol": "hive_usdt"})
        hive_usdt_response_json = self.validate_response(hive_usdt_response)

        if hive_usdt_response and hive_usdt_response_json:
            hive_usd_pair = hive_usdt_response_json["data"][0]["last"]

            price = round(float(hive_usd_pair), self.PRICE_PRECISION)
            self.logger.info(self.bundle_adapter_name(f'Price: {price}'))
            return price
