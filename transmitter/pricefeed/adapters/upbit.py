from .base import BaseAdapter
import requests


class UpbitAdapter(BaseAdapter):

    BASE_URL = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1"

    def get_price(self):
        btc_steem_response = requests.get(
            self.BASE_URL, params={"code": "CRIX.UPBIT.BTC-STEEM"})
        btc_steem_response_json = self.validate_response(btc_steem_response)

        usd_btc_response = requests.get(
            self.BASE_URL, params={"code": "CRIX.UPBIT.USDT-BTC"}
        )
        usd_btc_response_json = self.validate_response(usd_btc_response)

        if btc_steem_response_json and usd_btc_response_json:
            btc_steem_pair = btc_steem_response_json[0]["tradePrice"]
            usd_btc_pair = usd_btc_response_json[0]["tradePrice"]

            price = round(usd_btc_pair * btc_steem_pair, self.PRICE_PRECISION)
            self.logger.info(self.bundle_adapter_name(f'Price: {price}'))
            return price
