import json
import time
from datetime import datetime, timedelta
from http.client import HTTPSConnection
from urllib.parse import quote_plus


class LastChangeType:
    """
    string (lastChangedType.pay-order-seller)
    최종 변경 구분. 250바이트 내외

    PAY_WAITING	결제 대기
    PAYED	결제 완료
    EXCHANGE_OPTION	옵션 변경
    DELIVERY_ADDRESS_CHANGED	배송지 변경
    GIFT_RECEIVED	선물 수락
    CLAIM_REJECTED	클레임 철회
    DISPATCHED	발송 처리
    CLAIM_REQUESTED	클레임 요청
    COLLECT_DONE	수거 완료
    CLAIM_HOLDBACK_RELEASED	클레임 보류 해제
    CLAIM_COMPLETED	클레임 완료
    PURCHASE_DECIDED	구매 확정
    HOPE_DELIVERY_INFO_CHANGED	배송 희망일 변경
    CLAIM_REDELIVERING	교환 재배송처리
    """
    PAY_WAITING = 'PAY_WAITING'
    PAYED = 'PAYED'
    EXCHANGE_OPTION = 'EXCHANGE_OPTION'
    DELIVERY_ADDRESS_CHANGED = 'DELIVERY_ADDRESS_CHANGED'
    GIFT_RECEIVED = 'GIFT_RECEIVED'
    CLAIM_REJECTED = 'CLAIM_REJECTED'
    DISPATCHED = 'DISPATCHED'
    CLAIM_REQUESTED = 'CLAIM_REQUESTED'
    COLLECT_DONE = 'COLLECT_DONE'
    CLAIM_HOLDBACK_RELEASED = 'CLAIM_HOLDBACK_RELEASED'
    CLAIM_COMPLETED = 'CLAIM_COMPLETED'
    PURCHASE_DECIDED = 'PURCHASE_DECIDED'
    HOPE_DELIVERY_INFO_CHANGED = 'HOPE_DELIVERY_INFO_CHANGED'
    CLAIM_REDELIVERING = 'CLAIM_REDELIVERING'


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

    def __init__(self, conn: HTTPSConnection, headers: dict):
        '''
        네이버 쇼핑 주문 관리 클래스
        :param access_token: 네이버 쇼핑 API 접근 토큰
        '''
        self.conn = conn
        self.headers = headers

    def get_changed_orders(self, last_changed_from, last_changed_type=None):
        """
        example code:
            import http.client
            conn = http.client.HTTPSConnection("api.commerce.naver.com")
            headers = { 'Authorization': "Bearer REPLACE_BEARER_TOKEN" }
            conn.request("GET", "/external/v1/pay-order/seller/product-orders/last-changed-statuses?lastChangedFrom=2022-04-11T15%3A21%3A44.000%2B09%3A00&lastChangedTo=SOME_STRING_VALUE&lastChangedType=SOME_STRING_VALUE&moreSequence=SOME_STRING_VALUE&limitCount=SOME_INTEGER_VALUE", headers=headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
        """
        order_url = f'/external/v1/pay-order/seller/product-orders/last-changed-statuses'

        last_changed_to = last_changed_from + timedelta(days=1)
        #만일 last_changed_to가 현재 시간보다 미래라면 현재 시간의 1분 전으로 변경
        if last_changed_to > datetime.now():
            last_changed_to = datetime.now() - timedelta(minutes=1)

        # ISO 8601 형식으로 날짜 변환
        last_changed_from = last_changed_from.strftime('%Y-%m-%dT%H:%M:%S.000+09:00')
        last_changed_to = last_changed_to.strftime('%Y-%m-%dT%H:%M:%S.000+09:00')

        # URL 인코딩
        encoded_last_changed_from = quote_plus(last_changed_from) # 최대 24시간 이전의 주문 조회
        encoded_last_changed_to = quote_plus(last_changed_to)

        query = f"lastChangedFrom={encoded_last_changed_from}&lastChangedTo={encoded_last_changed_to}"
        if last_changed_type:
            query += f"&lastChangedType={last_changed_type}"

        self.conn.request("GET", f"{order_url}?{query}", headers=self.headers)

        response = self.conn.getresponse()
        if response.status != 200:
            raise Exception(f'Order Error: {response.status}, {response.read()}')

        data = response.read().decode('utf-8')
        json_data = json.loads(data)

        if json_data.get('data') is None:
            return []

        return [status.get('productOrderId') for status in json_data.get('data').get('lastChangeStatuses', [])]

    def get_weekly_orders(self):
        days = 2
        orders_by_date = {}
        # 오늘 00시 00분 00초부터 days일 전까지의 주문 조회
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)

        for day in range(days+1):
            day_from = start_date + timedelta(days=day)
            orders = self.get_changed_orders(last_changed_from=day_from, last_changed_type=LastChangeType.PAYED)
            orders_by_date[day_from.strftime('%Y-%m-%d')] = orders
            time.sleep(0.5)

        return orders_by_date
