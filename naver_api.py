import http

from auth.token_manager import get_token
from domain.order.order_manager import NaverOrderManager

access_token = get_token()

order_manager = NaverOrderManager()

def get_connection():
    conn = http.client.HTTPSConnection("api.commerce.naver.com")
    headers = {'Authorization': f'Bearer {access_token}'}
    return conn, headers