from requests import get, post, Response


class Client:
    @staticmethod
    def get(url, params=None) -> Response:
        response = get(url, params=params)
        return response

    @staticmethod
    def post(url, data=None, params=None):
        response = post(url, data=data, params=params)
        return response

