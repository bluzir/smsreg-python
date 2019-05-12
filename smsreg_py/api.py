import logging
from typing import Union

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

    # Activation methods
    def get_num(self, country: str, service: str) -> dict:
        """
        Method for requesting number for specific country and service.

        Documentation: https://sms-reg.com/docs/APImethods.html?getNum

        :param country: string (all, ru, ua, kz, cn)
        :param service: string (list of services is available in doc)
        :return: dict: json from API-response
        """
        params = {
            'country': country,
            'service': service,
            **self.params
        }
        response = self._get_api('getNum', params)
        return response

    def get_balance(self) -> dict:
        """
        Method for getting balance of account

        Documentation: https://sms-reg.com/docs/APImethods.html?getBalance

        :return: dict: json from API-response
        """
        response = self._get_api('getBalance', self.params)
        return response

    def set_ready(self, tzid: Union[int, str]) -> dict:
        """
        Method for setting transaction to ready state
        :param tzid: int/str (transaction_id)
        :return: dict: json from API-response
        """
        params = {
            'tzid': tzid,
            **self.params,
        }
        response = self._get_api('setReady', params=params)
        return response

    def get_state(self, tzid: Union[int, str]) -> dict:
        """
        Method for getting transaction state by its ID

        Documentation: https://sms-reg.com/docs/APImethods.html?getState

        :param tzid: int/str (transaction_id)

        :return: dict: json from API-response
        """
        params = {
            'tzid': tzid,
            **self.params,
        }
        response = self._get_api('getState', params=params)
        return response

    def get_operations(self,
                       opstate: str ='active',
                       count: Union[int, str] = 100,
                       output: str = 'array') -> dict:
        """
        Method for getting list of operations for account

        Documentation: https://sms-reg.com/docs/APImethods.html?getOperations

        :param opstate: str: filter by state (active/completed)
        :param count: int/str: number of operations to returb
        :param output: response format (array/object)

        :return: dict: json from API-response
        """
        params = {
            'opstate': opstate,
            'count': count,
            'output': output,
            **self.params
        }
        response = self._get_api('getOperations', params=params)
        return response

    def get_list(self) -> dict:
        """
        Method for getting list of available services with sms-codes

        Documentation: https://sms-reg.com/docs/APImethods.html?getList

        :return: dict: json from API-response
        """
        response = self._get_api('getList', self.params)
        return response

    def set_operation(self,
                      tzid: Union[int, str],
                      otype: str = 'ok') -> dict:
        """
        Method for changing operation status after

        Documentation OK: https://sms-reg.com/docs/APImethods.html?setOperationOk
        Documentation USED: https://sms-reg.com/docs/APImethods.html?setOperationUsed

        :param tzid: int/str: transaction id
        :param otype: str: new status (ok/used)

        :return: dict: json from API-response
        """

        if otype == 'ok':
            method = 'setOperationOk'
        elif otype == 'used':
            method = 'setOperationUsed'
        else:
            return {}

        params = {
            'tzid': tzid,
            **self.params
        }

        response = self._get_api(method, params)
        return response

    # VirtualSIM methods
    def vsim_get(self, country, period):
        """
        Method for requesting VirtualSIM number

        Documentation: https://sms-reg.com/docs/APImethods.html?vsimGet
        :param country: str: country name (ru, ua, gb, bg, pl, hk)
        :param period: str: period of rent (3hours, day, week)

        :return: dict: json from API-response
        """
        params = {
            'country': country,
            'period': period,
            **self.params
        }

        response = self._get_api('vsimGet', params)
        return response

    def vsim_get_sms(self, number: int):
        """
        Method for getting sms from VirtualSIM number that you renting

        Documentation: https://sms-reg.com/docs/APImethods.html?vsimGetSMS

        :param number: int/str: number that you renting

        :return: dict: json from API-response
        """
        params = {
            'number': number,
            **self.params
        }

        response = self._get_api('vsimGetSMS', params)
        return response

    # Base methods
    def _get_api(self, method: str, params: dict) -> dict:
        """
        Base method to send GET-request to API

        :param method: str: API-method name
        :param params: dict: url-params

        :return: dict: json from API-response
        """
        url = self.API_URL.format(self.BASE_URL, method)
        response = self.get(url, params=params)
        if response:
            decoded = response.json()
            logging.debug(decoded)
            return decoded
        else:
            raise Exception

    def _post_api(self, method: str, data: dict, params: dict) -> dict:
        """
        Base method to send POST-request to API

        :param method: str: API-method name
        :param params: dict: url-params
        :param data: dict: post-params

        :return: dict: json from API-response
        """
        url = self.API_URL.format(self.BASE_URL, method)
        response = self.post(url, data=data, params=params)
        if response:
            decoded = response.json()
            logging.debug(decoded)
            return decoded
        else:
            raise Exception
