import logging
from time import sleep
from typing import NoReturn

from smsreg_py.api import SmsRegClient

from smsreg_py.config import MINIMAL_BALANCE


class SmsReg(SmsRegClient):
    country = 'ru'  # all, ru, ua, kz, cn

    def __init__(self):
        super(SmsReg, self).__init__()
        self.services = {}
        self._check_balance()
        self._get_services_list()

        self.tz_id = None

    def request_number(self, service) -> bool:
        if service in self.services:
            response = self.get_num(self.country, service)
            result = response['response']
            print(response)
            if result == '1':
                self.tz_id = response['tzid']
                return True
        return False

    def get_number_from_transaction(self) -> str:
        number = None
        while not number:
            response = self.get_state(self.tz_id)
            status = response['response']
            if status == 'TZ_NUM_PREPARE':
                number = response['number']
            elif status == 'WARNING_NO_NUMS':
                raise Exception
            sleep(3)
        return number

    def get_code_from_transaction(self) -> str:
        code = None
        while not code:
            response = self.get_state(self.tz_id)
            status = response['response']
            if status == 'TZ_NUM_ANSWER':
                code = response['msg']
            sleep(3)
        return code

    def set_transaction_ready(self):
        response = self.set_ready(self.tz_id)
        status = response['response']
        if status == 1:
            return True
        return False

    def set_transaction_ok(self) -> bool:
        response = self.set_operation('ok')
        status = response['response']
        if status == 1:
            return True
        return False

    def set_transaction_used(self) -> bool:
        response = self.set_operation('used')
        status = response['response']
        if status == 1:
            return True
        return False

    def _check_balance(self) -> bool:
        response = self.get_balance()
        balance = float(response['balance'])
        logging.info(f'Current balance: {balance} RUB')
        if balance < MINIMAL_BALANCE:
            raise Exception
        return True

    def _get_services_list(self) -> NoReturn:
        response = self.get_list()
        services_dict = response['services']
        services_list = [s['service'] for s in services_dict]
        self.services = services_list
        logging.debug('Parsed {} service names'.format(len(services_list)))





