from smsreg_py.config import API_KEY
from smsreg_py.base import Client


class SmsRegClient(Client):
    """
    Sms-REG base API wrapper
    """
    BASE_URL = 'http://api.sms-reg.com/'
    API_URL = '{}{}.php'

    def __init__(self, api_key=None):
        self.api_key = api_key or API_KEY
        self.params = {
            'apikey': self.api_key
        }

    def get_num(self, country: str, service: str) -> dict:
        params = {
            'country': country,
            'service': service,
            **self.params
        }
        response = self._get_api('getNum', params)
        return response

    def get_balance(self) -> dict:
        response = self._get_api('getBalance', self.params)
        return response

    def set_ready(self, tzid: str) -> dict:
        params = {
            'tzid': tzid,
            **self.params,
        }
        response = self._get_api('setReady', params=params)
        return response

    def get_state(self, tzid: str) -> dict:
        params = {
            'tzid': tzid,
            **self.params,
        }
        response = self._get_api('getState', params=params)
        return response

    def get_operations(self,
                       opstate='active',
                       count=100,
                       output='array') -> dict:
        params = {
            'opstate': opstate,
            'count': count,
            'output': output,
            **self.params
        }
        response = self._get_api('getOperations', params=params)
        return response

    def get_list(self):
        response = self._get_api('getList', self.params)
        return response

    def set_operation(self, tzid: str, otype: str = 'ok') -> dict:
        if otype == 'ok':
            method = 'setOperationOk'
        elif otype == 'revise':
            method = 'setOperationRevise'
        elif otype == 'over':
            method = 'setOperationOver'
        else:
            return {}

        params = {
            'tzid': tzid,
            **self.params
        }

        response = self._get_api(method, params)
        return response

    def _get_api(self, method: str, params: dict) -> dict:
        url = self.API_URL.format(self.BASE_URL, method)
        response = self.get(url, params=params)
        if response:
            return response.json()
        else:
            return {}

    def _post_api(self, method: str, data: dict, params: dict) -> dict:
        url = self.API_URL.format(self.BASE_URL, method)
        response = self.post(url, data=data, params=params)
        if response:
            response.json()
        else:
            return {}
