import logging

from smsreg_py.smsreg import SmsReg


def main():
    sms_client.request_number('telegram')
    number = sms_client.get_number_from_transaction()
    print(f'Your number is: {number}')
    input('Enter anything after entering number to telegram')
    sms_client.set_transaction_ready()
    print('Waiting for sms...')
    code = sms_client.get_code_from_transaction()
    result = input(f'Code is {code}. Is it valid? (y/n)')
    if result == 'y':
        sms_client.set_transaction_ok()
    if result == 'n':
        sms_client.set_transaction_used()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sms_client = SmsReg()
    main()
