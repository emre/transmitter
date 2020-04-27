from .base import BaseAdapter
import requests


class BinanceAdapter(BaseAdapter):

    BASE_URL = "https://api.binance.com/api/v3/ticker/price"

    def get_price(self):
        hive_usdt_response = requests.get(
            self.BASE_URL, params={"symbol": "HIVEUSDT"}

        )
        hive_usdt_response_json = self.validate_response(hive_usdt_response)

        if hive_usdt_response_json:
            hive_usdt_price = float(hive_usdt_response_json["price"])
            price = round(hive_usdt_price, self.PRICE_PRECISION)
            self.logger.info(self.bundle_adapter_name(f'Price: {price}'))
            return price
