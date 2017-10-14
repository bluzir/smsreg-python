import requests


class Client:
    def get_request(self, url, params=None):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response
        else:
            return False

    def post_request(self, url, data=None, params=None):
        response = requests.post(url, data=data, params=params)
        if response.status_code == 200:
            return response
        else:
            return False

