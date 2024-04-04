import http
import json
import time
from datetime import datetime, timedelta
from http.client import HTTPSConnection
from urllib.parse import quote_plus


class NaverOrderManager:
    """
    NaverOrderManager: 네이버 쇼핑 주문 관리 클래스
    주요 속성:
        access_token: 네이버 쇼핑 API 접근 토큰
        headers: 네이버 쇼핑 API 접근 헤더

    주요 메서드:
        get_new_orders: 특정 시간 이후의 새로운 주문 조회
        confirm_orders: 주문 확인 처리
    """

    BASE_URL = 'https://api.commerce.naver.com/external/v1'

    def __init__(self, conn: HTTPSConnection, headers: dict):
        '''
        네이버 쇼핑 주문 관리 클래스
        :param access_token: 네이버 쇼핑 API 접근 토큰
        '''
        self.conn = conn
        self.headers = headers

    def get_new_orders(self, last_changed_from):
        order_url = f'/external/v1/pay-order/seller/product-orders/last-changed-statuses'

        # ISO 8601 형식으로 날짜 변환
        last_changed_from = last_changed_from.strftime('%Y-%m-%dT%H:%M:%S.000+09:00')

        # URL 인코딩
        encoded_last_changed_from = quote_plus(last_changed_from) # 최대 24시간 이전의 주문 조회

        self.conn.request("GET",
                          f"{order_url}?lastChangedFrom={encoded_last_changed_from}",
                          headers=self.headers)
        response = self.conn.getresponse()
        if response.status != 200:
            raise Exception(f'Order Error: {response.status}, {response.read()}')

        data = response.read().decode('utf-8')
        json_data = json.loads(data)

        if json_data.get('data') is None:
            return []

        return [status.get('productOrderId') for status in json_data.get('data').get('lastChangeStatuses', [])]

    def get_weekly_orders(self):
        orders_by_date = {}
        start_date = datetime.now() - timedelta(days=7)

        for day in range(7):
            day_from = start_date + timedelta(days=day)
            orders = self.get_new_orders(day_from)
            orders_by_date[day_from.strftime('%Y-%m-%d')] = orders
            time.sleep(0.3)

        return orders_by_date

        # return [status.get('productOrderId') for status in data.get('lastChangeStatuses', [])]

        # if response.status_code != 200:
        #     raise Exception(f'Order Error: {response.status_code}, {response.text}')
        #
        # data = response.json().get('data', {})
        # return [status.get('productOrderId') for status in data.get('lastChangeStatuses', [])]

    # def confirm_orders(self, product_order_ids):
    #     confirm_url = f'{self.BASE_URL}/pay-order/seller/product-orders/confirm'
    #     max_count = 30
    #
    #     for i in range(0, len(product_order_ids), max_count):
    #         current_ids = product_order_ids[i:i + max_count]
    #         payload = {"productOrderIds": current_ids}
    #
    #         response = requests.post(confirm_url, json=payload, headers=self.headers)
    #
    #         if response.status_code != 200:
    #             raise Exception(f'Confirm Error: {response.status_code}, {response.text}')
    #
    #         print(f'Confirmation Data for IDs {i} to {i + max_count - 1} :', response.json())
