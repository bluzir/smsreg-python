from smsreg_python.smsreg import SmsReg


def main():
    sms_client = SmsReg()
    number = sms_client.get_virtualsim_number()
    print(f'Received number: {number}')

    sms_list = sms_client.get_virtualsim_sms_list()
    for item in sms_list:
        date = item['date']
        text = item['text']
        print(f'Date:{date}. Text: {text}')
