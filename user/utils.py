import requests

from django.conf import settings


def generate_oauth_token(username, password):
    """
    generating outh token
    """
    client_id = settings.OAUTH2_CLIENT_ID
    client_secret = settings.OAUTH2_CLIENT_SECRET
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': 'password',
               'username': username,
               'password': password,
               'client_id': client_id,
               'client_secret': client_secret}

    host = "http://localhost:8000"
    return (requests.post(
        host + "/o/token/",
        data=payload,
        headers=headers,
        verify=False))
