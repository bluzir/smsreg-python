from requests import Session, Response


class Client:
    @staticmethod
    def get(url, params=None) -> Response:
        with Session() as s:
            response = s.get(url, params=params)
        return response

    @staticmethod
    def post(url, data=None, params=None):
        with Session() as s:
            response = s.post(url, data=data, params=params)
        return response

