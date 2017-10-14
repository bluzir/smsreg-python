import config
from base_client import Client



class SmsRegClient(Client):
    APP_ID = 'qweqwe'
    BASE_URL = 'http://api.sms-reg.com/'
    API_URL = '{}{}.php'

    def __init__(self, api_key=None):
        self.api_key = api_key or config.API_KEY
        self.params = {
            'apikey': self.api_key
        }

    def get_num(self, country, service):
        params = {
            'country': country,
            'service': service,
            **self.params
        }
        response = self._get_api('getNum', params)
        return response

    def get_balance(self):
        response = self._get_api('getBalance', self.params)
        return response

    def set_ready(self, tzid):
        params = {
            'tzid': tzid,
            **self.params,
        }
        response = self._get_api('setReady', params=params)
        return response

    def get_state(self, tzid):
        params = {
            'tzid': tzid,
            **self.params,
        }
        response = self._get_api('getState', params=params)
        return response

    def get_operations(self, opstate='active', count=100, output='array'):
        params = {
            'opstate': opstate,
            'count': count,
            'output': output,
            **self.params
        }
        response = self._get_api('getOperations', params=params)
        return response

    def set_operation(self, tzid, type='ok'):
        if type == 'ok':
            method = 'setOperationOk'
        elif type == 'revise':
            method = 'setOperationRevise'
        elif type == 'over':
            method = 'setOperationOver'
        else:
            return False

        params = {
            'tzid': tzid,
            **self.params
        }

        response = self._get_api(method, params)
        return response

    def _get_api(self, method, params):
        url = self.API_URL.format(self.BASE_URL, method)
        response = self.get_request(url, params=params)
        if response:
            return response.json()
        else:
            return False

    def _post_api(self, method, data, params):
        url = self.API_URL.format(self.BASE_URL, method)
        response = self.post_request(url, data=data, params=params)
        if response:
            response.json()
        else:
            return False
