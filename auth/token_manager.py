import bcrypt
import pybase64
import requests
import time

BASE_URL = 'https://api.commerce.naver.com/external/v1/oauth2/token'

client_id = '6e8QDBd5Oi2CAE0WiijrXM'
client_secret = '$2a$04$XRkBhFNBXdNClAqPoDs.Iu'
token_type = 'SELF'
account_id = 'jinji-market'


def _get_timestamp():
    return int(time.time() * 1000)


def _get_client_secret_sign(client_id, client_secret, timestamp):
    password = f"{client_id}_{timestamp}"
    hashed = bcrypt.hashpw(password.encode('utf-8'), client_secret.encode('utf-8'))
    return pybase64.standard_b64encode(hashed).decode('utf-8')


def get_token():
    timestamp = _get_timestamp()
    client_secret_sign = _get_client_secret_sign(client_id, client_secret, timestamp)
    print(f'timestamp: {timestamp}, client_secret_sign: {client_secret_sign}')
    params = {
        'client_id': client_id,
        'timestamp': timestamp,
        'client_secret_sign': client_secret_sign,
        'grant_type': 'client_credentials',
        'type': token_type,
    }
    print(f'params: {params}')
    if token_type == 'SELLER':
        params['account_id'] = account_id
    time.sleep(1)
    response = requests.post(BASE_URL, data=params)
    print(f'response: {response.text}')
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


if __name__ == '__main__':
    try:
        access_token = get_token()
        print('Access Token:', access_token)
    except Exception as e:
        print(e)