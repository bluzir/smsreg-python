# smsreg-python

![Python 3.6|3.7](https://img.shields.io/badge/python-3.6%20%7C%203.7-blue.svg) 
![MIT](https://img.shields.io/pypi/l/smsreg-python.svg) 
![1.1.0](https://img.shields.io/pypi/v/smsreg-python.svg) 

Python client for receiving SMS from sms-reg.com.

# Installation 

`pip install smsreg_python --upgrade`

# Example

```python
from smsreg_python.smsreg import SmsReg
from smsreg_python.dataclasses import Services

API_KEY = "there must be api key"
# Creating SMS-client instance
sms_client = SmsReg(API_KEY)

# Requesting number
sms_client.request_number(Services.INSTAGRAM)

# Receiving number and code
number = sms_client.wait_number_from_transaction()
input('Enter anything after entering number to form')
code = sms_client.wait_code_from_transaction()

```

You can see other usage example in `examples`
