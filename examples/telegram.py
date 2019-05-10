from api import SmsRegClient

client = SmsRegClient()

def main():
    balance = client.get_balance()
    print(balance)


if __name__ == '__main__':
    main()