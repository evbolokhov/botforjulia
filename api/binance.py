import hmac
import hashlib
import time
import requests


class Binance_API():
    api_url = 'https://fapi.binance.com'
    api_key = None
    secret_key = None

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def getSignature(self, params):
        param_str = '&'.join([f'{k}={v}' for k, v in params.items()])
        hash = hmac.new(bytes(self.secret_key, 'utf-8'), param_str.encode('utf-8'), hashlib.sha256)

        return hash.hexdigest()

    def HTTP_Request(self, endpoint, method, params):
        header = {
            'X-MBX-APIKEY': self.api_key
        }
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self.getSignature(params)

        if method == 'GET':
            response = requests.get(url=self.api_url + endpoint, params=params, headers=header)

        elif method == 'POST':
            response = requests.post(url=self.api_url + endpoint, params=params, headers=header)

        return response.json()

    def get_candles(self, symbol, interval, limit=500):
        endPoint = '/fapi/v1/klines'
        method = 'GET'
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        return self.HTTP_Request(endpoint=endPoint, method=method, params=params)

    def create_market_order(self, symbol, side, qnt):
        endPoint = '/fapi/v1/order'
        method = 'POST'
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": qnt,
            "type": "MARKET"
        }
        return self.HTTP_Request(endpoint=endPoint, method=method, params=params)

    def create_limit_order(self, symbol, side, qnt, price, reduce_only=False):
        endPoint = '/fapi/v1/order'
        method = 'POST'
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": qnt,
            "type": "LIMIT",
            "price": price,
            "timeInForce": "GTC"
        }
        if reduce_only:
            params["reduceOnly"] = True

        return self.HTTP_Request(endpoint=endPoint, method=method, params=params)

    def create_take_profit(self, symbol, side, stopPrice):
        endPoint = '/fapi/v1/order'
        method = 'POST'
        params = {
            "symbol": symbol,
            "side": side,
            "type": "TAKE_PROFIT_MARKET",
            "stopPrice": stopPrice,
            "closePosition": True
        }
