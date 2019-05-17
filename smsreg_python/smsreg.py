import logging
from time import sleep
from typing import NoReturn

from smsreg_python.api import SmsRegClient

from smsreg_python.config import MINIMAL_BALANCE, SLEEP_TIME
from smsreg_python.dataclasses import TransactionStates


class SmsReg(SmsRegClient):
    country = 'ru'  # all, ru, ua, kz, cn

    def __init__(self, api_key=None):
        super(SmsReg, self).__init__(api_key=api_key)
        self.services = {}
        self._check_balance()
        self._get_services_list()

        # temporary storage
        self.tz_id = None
        self.virtual_number = None

    def request_number(self, service, app_id=None) -> bool:
        """
        Method for requesting phone number for specific service

        :param service: str – name of service from self.services
        :param app_id: str - if available, else leave blank

        :return: bool – True if API-response is OK, else False
        ID of successful transaction is stored in self.tz_id
        """
        if service in self.services:
            response = self.get_num(self.country, service, app_id)
            result = self._check_response(response)
            if result:
                self.tz_id = response['tzid']
            return result
        return False

    def get_and_check_transaction(self):
        """
        Method for getting state of transaction and check if it is valid
        :return: response: if transaction is valid
        """
        response = self.get_state(self.tz_id)
        status = response['response']
        if status in TransactionStates.GET_STATE_ERRORS:
            logging.info(f'Error: {status}')
            raise Exception
        if status in TransactionStates.GET_STATE_EXPIRED:
            logging.info(f'Session expired. Try again')
            raise OperationExpiredException
        if status in TransactionStates.GET_STATE_SUCCESS:
            return response
        else:
            return response

    def wait_number_from_transaction(self) -> str:
        """
        Method for extracting number from API for current transaction (self.tz_id).

        If API will return `WARNING_NO_NUMS`, an exception will be thrown

        :return: number – string with current number
        """
        number = None
        while not number:
            response = self.get_and_check_transaction()
            if 'number' in response:
                number = response['number']
            sleep(SLEEP_TIME)
        return number

    def wait_code_from_transaction(self) -> str:
        """
        Method for extracting sms-code from API for current transaction (self.tz_id).
        :return: code - string with current code
        """
        code = None
        while not code:
            response = self.get_and_check_transaction()
            if 'msg' in response:
                code = response['msg']
            sleep(SLEEP_TIME)
        return code

    def set_transaction_ok(self) -> bool:
        """
        Method for setting current transaction to `OK` status.
        You should call it after you enter registration code and it will be valid.
        :return: bool – True if API-response is OK, else False
        """
        response = self.set_operation('ok')
        return self._check_response(response)

    def set_transaction_used(self) -> bool:
        """
        Method for setting current transaction to `USED` status.
        You should call it after you enter phone and it has already been used in service.
        :return: bool – True if API-response is OK, else False
        """
        response = self.set_operation('used')
        return self._check_response(response)

    def get_virtualsim_number(self, period: str = '3hours') -> str:
        response = self.vsim_get(self.country, period)
        result = self._check_response(response)
        if result:
            number = response['number']
            self.virtual_number = number
            return self.virtual_number
        return ""

    def get_virtualsim_sms_list(self) -> list:
        response = self.vsim_get_sms(self.virtual_number)
        result = self._check_response(response)
        if result:
            return response['items']
        return []

    def _set_transaction_ready(self):
        """
        Deprecated method for setting current transaction status to `ready`.
        You may call it after entering phone number in registration form
        However now it works automatically

        :return: bool – True if API-response is OK, else False
        """
        response = self._set_ready(self.tz_id)
        return response

    def _check_balance(self) -> bool:
        """
        Method that calls after initialization to check current account balance.
        Balance should be > MINIMAL_BALANCE from config file.

        :return: True if balance is OK, else raises Exception
        """
        response = self.get_balance()
        balance = float(response['balance'])
        logging.info(f'Current balance: {balance} RUB')
        if balance < MINIMAL_BALANCE:
            raise Exception
        return True

    def _get_services_list(self) -> NoReturn:
        """
        Method that calls after initialization to get current services list from API.
        This list uses in `request_number` method for checking.

        """
        response = self.get_list()
        services_dict = response['services']
        services_list = [s['service'] for s in services_dict]
        self.services = services_list
        logging.debug('Parsed {} service names'.format(len(services_list)))

    @staticmethod
    def _check_response(response):
        if 'response' in response:
            status = response['response']
            if status == 'ERROR':
                raise Exception(response['error_msg'])
            if int(status) == 1:
                return True
        return False


class OperationExpiredException(Exception):
    def __init__(self):
        super(OperationExpiredException, self).__init__()
