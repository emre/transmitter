from .base import BaseAdapter
import requests


class ProbitAdapter(BaseAdapter):

    BASE_URL = "https://api.probit.com/api/exchange/v1/ticker"

    def get_price(self):
        ticker_data = requests.get(
            self.BASE_URL,
            params={"market_ids": "BTC-USDT,HIVE-BTC"})

        ticker_response = self.validate_response(ticker_data).get("data", [])

        usd_btc_response = [
            r for r in ticker_response if r["market_id"] == "BTC-USDT"][0]

        btc_hive_response = [
            r for r in ticker_response if r["market_id"] == "HIVE-BTC"][0]

        btc_hive_pair = btc_hive_response["last"]
        usd_btc_pair = usd_btc_response["last"]

        price = round(float(usd_btc_pair) * float(btc_hive_pair), self.PRICE_PRECISION)
        self.logger.info(self.bundle_adapter_name(f'Price: {price}'))
        return price
