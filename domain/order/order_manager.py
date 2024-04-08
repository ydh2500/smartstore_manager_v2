import json
import time
import traceback
from datetime import datetime, timedelta
from http.client import HTTPSConnection
from urllib.parse import quote_plus

from pydantic import ValidationError

from domain.order.order_schema import LastChangeStatus, LastChangeStatusList


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

    def get_changed_orders(self, last_changed_from: datetime, last_changed_type: str = None):
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
        last_change_statuses = LastChangeStatusList(lastChangeStatus_list=[])

        last_changed_from = last_changed_from.replace(hour=0, minute=0, second=0, microsecond=0)
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
            return last_change_statuses

        try:
            for status in json_data.get('data')['lastChangeStatuses']:
                try:
                    last_change_status = LastChangeStatus(**status)
                    last_change_statuses.lastChangeStatus_list.append(last_change_status)
                except ValidationError as e:
                    print(f'error: {e.json()}')
                    print(f'status: {status}')
        except ValidationError as e:
            print(e.json())

        return last_change_statuses

    def get_orders_for_days(self, since_from: datetime, last_changed_type: str):
        # LastChangeStatusList 객체 생성
        all_orders = LastChangeStatusList(lastChangeStatus_list=[])

        # since_from 부터 현재 까지의 주문 조회
        start_date = since_from.replace(hour=0, minute=0, second=0, microsecond=0)
        days = (datetime.now() - start_date).days

        for day in range(days + 1):
            day_from = start_date + timedelta(days=day)
            orders = self.get_changed_orders(last_changed_from=day_from, last_changed_type=last_changed_type)
            # 각 날짜별로 얻은 주문을 all_orders에 추가
            all_orders.lastChangeStatus_list.extend(orders.lastChangeStatus_list)
            time.sleep(0.4)

        return all_orders