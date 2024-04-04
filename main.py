import traceback
from datetime import datetime, timedelta
import http.client
from auth.token_manager import get_token
from order_manager import NaverOrderManager

if __name__ == '__main__':
    CLIENT_ID = '6e8QDBd5Oi2CAE0WiijrXM'
    CLIENT_SECRET = '$2a$04$XRkBhFNBXdNClAqPoDs.Iu'
    TOKEN_TYPE = 'SELF'
    ACCOUNT_ID = 'jinji-market'

    access_token = get_token()

    conn = http.client.HTTPSConnection("api.commerce.naver.com")
    headers = {'Authorization': f'Bearer {access_token}'}

#    token_manager = TokenManager(CLIENT_ID, CLIENT_SECRET, TOKEN_TYPE, ACCOUNT_ID)

    order_manager = NaverOrderManager(conn, headers)
    since_from_datetime = datetime.now() - timedelta(days=30)

    try:
        new_orders = order_manager.get_new_orders(since_from_datetime)
        print('New Orders:', new_orders)

        new_orders = order_manager.get_weekly_orders()
        print('Weekly Orders:', new_orders)
        # order_manager.confirm_orders(new_orders)
    except Exception as e:
        print(f'Order Error: {e}')
        traceback.print_exc()