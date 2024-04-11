import http

from auth.token_manager import get_token

access_token = get_token()


def get_connection():
    conn = http.client.HTTPSConnection("api.commerce.naver.com")
    headers = {'Authorization': f'Bearer {access_token}'}
    return conn, headers