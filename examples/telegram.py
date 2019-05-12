from smsreg_python.smsreg import SmsReg
from smsreg_python.dataclasses import Services


def main():
    service = Services.TELEGRAM
    print(f'Requesting number for {service}')
    sms_client.request_number(Services.TELEGRAM)

    print(f'Waiting for number')
    number = sms_client.wait_number_from_transaction()
    print(f'Your number is: {number}')

    input('Enter anything after entering number to telegram')
    print('Waiting for sms...')
    code = sms_client.wait_code_from_transaction()
    result = input(f'Code is {code}. Is it valid? (y/n)')
    if result == 'y':
        sms_client.set_transaction_ok()
    if result == 'n':
        # sms_client.set_transaction_used()
        print('Something gone wrong')


if __name__ == '__main__':
    sms_client = SmsReg()
    main()
