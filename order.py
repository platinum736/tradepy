import requests


class Order:
    def __init__(self,id):
        self.order_id = id


    def modify_order(self, access_token, modify_doc):
         # access_token=None, quantity=None, price=None, order_type=None,
         #           transaction_type=None, trigger_price=None, validity=None):

        url = "https://api.upstox.com/v2/order/modify"
        payload = dict()
        payload['order_id'] = self.order_id
        for key in ['quantity','price','order_type','transaction_type','trigger_price','validity']:
            if key in modify_doc:
                payload[key] = modify_doc[key]

        headers = {
            'Authorization' : 'Bearer '+ access_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}


    def cancel_order(self,access_token):
        url = "https://api.upstox.com/v2/order/cancel"
        url = url + "?order_id=" + self.order_id

        payload={}
        headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer '+ access_token
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        if response.status_code == 200:
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}


    def get_order_details(self,access_token):
        url = "https://api.upstox.com/v2/order/details"

        payload={}
        headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer '+ access_token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return response.json()['data']
        else:
            return {'Error':response.status_code,
                    'message':response.text}
