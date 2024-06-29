import requests
from dotenv import load_dotenv
load_dotenv()
import os
from order import Order

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")

class Upstox():
    code = '***'
    __access_token = None
    orders = list()


    def __init__(self,code):
        self.code = code
        if 'Error' in self.__set_api_token():
            print('Error in getting access token')

    def __set_api_token(self):
        url = 'https://api.upstox.com/v2/login/authorization/token'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'code': self.code,
            'client_id': API_KEY,
            'client_secret': API_SECRET,
            'redirect_uri': 'https://www.google.com',
            'grant_type': 'authorization_code',
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            self.__access_token = response.json()['access_token']
            return response.json()
        else:
            return {'Error':response.status_code,
                    'message':response.text}


    def logout(self):
        url = "https://api.upstox.com/v2/logout"

        payload={}
        headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer '+ self.__access_token
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}
    

    def get_profile(self):

        url = "https://api.upstox.com/v2/user/profile"

        payload={}
        headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer '+ self.__access_token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}


    def get_fund(self):
        url = "https://api.upstox.com/v2/user/get-funds-and-margin?segment=SEC"
        
        payload={}
        headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer '+ self.__access_token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}
    

    def get_days_trade(self):

        url = "https://api.upstox.com/v2/order/trades/get-trades-for-day"

        payload={}
        headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer '+ self.__access_token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}


    def place_order(self,quantity,product,price,instrument_token,order_type,
                    transaction_type,trigger_price,is_amo,validity="DAY"):
        url = "https://api.upstox.com/v2/order/place"

        payload = {
            "quantity": quantity,
            "product": product,
            "price":price,
            "validity":validity, # DAY|IOC
            "instrument_token": instrument_token,
            "order_type": order_type, # LIMIT|MARKET|SL|SL-M
            "transaction_type": transaction_type, # BUY|SELL,
            "disclosed_quantity":quantity,
            "trigger_price":trigger_price,
            "is_amo":is_amo # after market order
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization' : 'Bearer '+ self.__access_token
        }
        print(payload)
        response = requests.request("POST", url, headers=headers, json=payload)
        if response.status_code == 200:
            self.orders.append(Order(response.json()['data']['order_id']))
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}

    def get_historical_data(self,instrument_token,interval,end_date,st_date=None):
        if interval not in ['1minute','30minute', 'day', 'week', 'month']:
            return {
                "Error":"interval should be in ['1minute','30minute', 'day', 'week', 'month']"
            }

        url = "https://api.upstox.com/v2/historical-candle/" + instrument_token + '/' + interval + '/'
        url = url + end_date
        if st_date:
            url = url + '/' + st_date


        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer '+ self.__access_token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}


    def get_ltp(self,instrument_token):

        url = "https://api.upstox.com/v2/market-quote/ltp"

        payload = {
            'instrument_key':instrument_token
        }
        headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer '+ self.__access_token
        }

        response = requests.request("GET", url, headers=headers, params=payload)

        if response.status_code == 200:
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}


    def get_intrday_ohlc(self,instrument_token,interval):
        url = "https://api.upstox.com/v2/historical-candle/intraday/"
        if interval not in ['1minute','30minute']:
            return {
                "Error":"interval should be in ['1minute','30minute']"
            }
        url = url + instrument_token + '/' + interval

        headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer '+ self.__access_token
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}


    def get_option_contracts(self,instrument_token,expiry_date):

        url = "https://api.upstox.com/v2/option/contract"

        payload = {
            'instrument_key':instrument_token,
            'expiry_date':expiry_date
        }

        headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer '+ self.__access_token
        }

        response = requests.request("GET", url, headers=headers, params=payload)

        if response.status_code == 200:
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}