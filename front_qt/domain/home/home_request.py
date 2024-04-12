import requests
from datetime import datetime

# API 서버의 URL 설정
BASE_URL = "http://127.0.0.1:8000/api/order"

def get_all_changed_list(since_from: str):
    """모든 변경된 주문 리스트를 가져옵니다."""
    url = f"{BASE_URL}/all_changed_list"
    params = {'since_from': since_from}
    response = requests.get(url, params=params)
    return response.json()

def get_pay_waiting_list(since_from: str):
    """결제 대기 중인 주문 리스트를 가져옵니다."""
    url = f"{BASE_URL}/pay_waiting_list"
    params = {'since_from': since_from}
    response = requests.get(url, params=params)
    return response.json()

def get_payed_list(since_from: str):
    """결제 완료된 주문 리스트를 가져옵니다."""
    url = f"{BASE_URL}/payed_list"
    params = {'since_from': since_from}
    response = requests.get(url, params=params)
    return response.json()

def get_purchase_decided_list(since_from: str):
    """구매 확정된 주문 리스트를 가져옵니다."""
    url = f"{BASE_URL}/purchase_decided_list"
    params = {'since_from': since_from}
    response = requests.get(url, params=params)
    return response.json()

def get_order_detail_list(product_order_ids: list):
    """특정 상품 주문 ID에 대한 상세 정보를 가져옵니다."""
    url = f"{BASE_URL}/order_detail_list"
    params = {'product_order_ids': ','.join(product_order_ids)}
    response = requests.get(url, params=params)
    return response.json()

# 예제 함수 사용
if __name__ == "__main__":
    since_from = datetime.now().strftime('%Y-%m-%d')  # ISO 8601 포맷
    print("All Changed List:", get_all_changed_list(since_from))
    print("Pay Waiting List:", get_pay_waiting_list(since_from))
    print("Payed List:", get_payed_list(since_from))
    print("Purchase Decided List:", get_purchase_decided_list(since_from))
    print("Order Detail List:", get_order_detail_list(['1234567890']))