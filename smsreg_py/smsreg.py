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

        # temporary storage
        self.tz_id = None
        self.virtual_number = None

    def request_number(self, service) -> bool:
        """
        Method for requesting phone number for specific service
        :param service: str – name of service from self.services
        :return: bool – True if API-response is OK, else False
        ID of successful transaction is stored in self.tz_id
        """
        if service in self.services:
            response = self.get_num(self.country, service)
            result = response['response']
            if result == '1':
                self.tz_id = response['tzid']
                return True
        return False

    def get_number_from_transaction(self) -> str:
        """
        Method for extracting number from API for current transaction (self.tz_id).

        If API will return `WARNING_NO_NUMS`, an exception will be thrown

        :return: number – string with current number
        """
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
        """
        Method for extracting sms-code from API for current transaction (self.tz_id).
        :return: code - string with current code
        """
        code = None
        while not code:
            response = self.get_state(self.tz_id)
            status = response['response']
            if status == 'TZ_NUM_ANSWER':
                code = response['msg']
            sleep(3)
        return code

    def set_transaction_ready(self):
        """
        Method for setting current transaction status to `ready`.
        You should call it after entering phone number in registration form.
        :return:
        """
        response = self.set_ready(self.tz_id)
        status = response['response']
        if status == 1:
            return True
        return False

    def set_transaction_ok(self) -> bool:
        """
        Method for setting current transaction to `OK` status.
        You should call it after you enter registration code and it will be valid.
        :return: bool – True if API-response is OK, else False
        """
        response = self.set_operation('ok')
        status = response['response']
        if status == 1:
            return True
        return False

    def set_transaction_used(self) -> bool:
        """
        Method for setting current transaction to `USED` status.
        You should call it after you enter phone and it has already been used in service.
        :return: bool – True if API-response is OK, else False
        """
        response = self.set_operation('used')
        status = response['response']
        if status == 1:
            return True
        return False

    def request_virtualsim_number(self, period: str = '3hours') -> bool:
        response = self.vsim_get(self.country, period)
        status = int(response['response'])
        if status == 1:
            self.virtual_number = response['number']
            return True
        return False

    def virtualsim_get_sms_list(self) -> list:
        response = self.vsim_get_sms(self.virtual_number)
        status = int(response['response'])
        if status == 1:
            return response['items']
        return []

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
        :return:
        """
        response = self.get_list()
        services_dict = response['services']
        services_list = [s['service'] for s in services_dict]
        self.services = services_list
        logging.debug('Parsed {} service names'.format(len(services_list)))


class ServiceConstants:
    """
    Constants class
    """
    AOL = 'aol'
    GMAIL = 'gmail'
    FACEBOOK = 'facebook'
    MAILRU = 'mailru'
    VK = 'vk'
    CLASSMATES = 'classmates'
    TWITTER = 'twitter'
    MAMBA = 'mamba'
    UBER = 'uber'
    TELEGRAM = 'telegram'
    BADOO = 'badoo'
    DRUGVOKRUG = 'drugvokrug'
    AVITO = 'avito'
    OLX = 'olx'
    STEAM = 'steam'
    FOTOSTRANA = 'fotostrana'
    MICROSOFT = 'microsoft'
    VIBER = 'viber'
    WHATSAPP = 'whatsapp'
    WECHAT = 'wechat'
    SEOSPRINT = 'seosprint'
    INSTAGRAM = 'instagram'
    YAHOO = 'yahoo'
    LINEME = 'lineme'
    KAKAOTALK = 'kakaotalk'
    MEETME = 'meetme'
    TINDER = 'tinder'
    NIMSES = 'nimses'
    YOULA = 'youla'
    _5KA = '5ka'
    OTHER = 'other'
