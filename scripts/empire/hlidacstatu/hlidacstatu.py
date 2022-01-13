import requests

from .subsidies import fetch_subsidies

class Hlidacstatu:
    def __init__(self, auth_token):
        self.auth_token = auth_token

        headers = {
            'Authorization': 'Token ' + auth_token,
            'Content-Type': 'text/plain'
        }
        r = requests.get('https://www.hlidacstatu.cz/api/v2/ping/test', headers=headers)

        if r.status_code != 200 and r.text != "pong test":
            raise Exception('Failed to connect to Hlidacstatu with provided AUTH token')

    def fetch_subsidies(self, legal_entities):
        return fetch_subsidies(self.auth_token, legal_entities)
