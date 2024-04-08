import datetime

from pydantic import BaseModel, validator


class LastChangedType:
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


class ProductOrderStatus:
    """
    string (productOrderStatus.pay-order-seller)
    상품 주문 상태. 250바이트 내외
    PAYMENT_WAITING	결제 대기
    PAYED	결제 완료
    DELIVERING	배송 중
    DELIVERED	배송 완료
    PURCHASE_DECIDED	구매 확정
    EXCHANGED	교환
    CANCELED	취소
    RETURNED	반품
    CANCELED_BY_NOPAYMENT	미결제 취소
    """
    PAYMENT_WAITING = 'PAYMENT_WAITING'
    PAYED = 'PAYED'
    DELIVERING = 'DELIVERING'
    DELIVERED = 'DELIVERED'
    PURCHASE_DECIDED = 'PURCHASE_DECIDED'
    EXCHANGED = 'EXCHANGED'
    CANCELED = 'CANCELED'
    RETURNED = 'RETURNED'
    CANCELED_BY_NOPAYMENT = 'CANCELED_BY_NOPAYMENT'


class ChangeType:
    """
    string (claimType.pay-order-seller)
    클레임 구분. 250바이트 내외

    CANCEL	취소
    RETURN	반품
    EXCHANGE	교환
    PURCHASE_DECISION_HOLDBACK	구매 확정 보류
    ADMIN_CANCEL	직권 취소
    """
    CANCEL = 'CANCEL'
    RETURN = 'RETURN'
    EXCHANGE = 'EXCHANGE'
    PURCHASE_DECISION_HOLDBACK = 'PURCHASE_DECISION_HOLDBACK'
    ADMIN_CANCEL = 'ADMIN_CANCEL'


class ClaimStatus:
    """
    string (claimStatus.pay-order-seller)
    클레임 상태. 250바이트 내외

    CANCEL_REQUEST	취소 요청
    CANCELING	취소 처리 중
    CANCEL_DONE	취소 처리 완료
    CANCEL_REJECT	취소 철회
    RETURN_REQUEST	반품 요청
    EXCHANGE_REQUEST	교환 요청
    COLLECTING	수거 처리 중
    COLLECT_DONE	수거 완료
    EXCHANGE_REDELIVERING	교환 재배송 중
    RETURN_DONE	반품 완료
    EXCHANGE_DONE	교환 완료
    RETURN_REJECT	반품 철회
    EXCHANGE_REJECT	교환 철회
    PURCHASE_DECISION_HOLDBACK	구매 확정 보류
    PURCHASE_DECISION_REQUEST	구매 확정 요청
    PURCHASE_DECISION_HOLDBACK_RELEASE	구매 확정 보류 해제
    ADMIN_CANCELING	직권 취소 중
    ADMIN_CANCEL_DONE	직권 취소 완료
    ADMIN_CANCEL_REJECT	직권 취소 철회
    """
    CANCEL_REQUEST = 'CANCEL_REQUEST'
    CANCELING = 'CANCELING'
    CANCEL_DONE = 'CANCEL_DONE'
    CANCEL_REJECT = 'CANCEL_REJECT'
    RETURN_REQUEST = 'RETURN_REQUEST'
    EXCHANGE_REQUEST = 'EXCHANGE_REQUEST'
    COLLECTING = 'COLLECTING'
    COLLECT_DONE = 'COLLECT_DONE'
    EXCHANGE_REDELIVERING = 'EXCHANGE_REDELIVERING'
    RETURN_DONE = 'RETURN_DONE'
    EXCHANGE_DONE = 'EXCHANGE_DONE'
    RETURN_REJECT = 'RETURN_REJECT'
    EXCHANGE_REJECT = 'EXCHANGE_REJECT'
    PURCHASE_DECISION_HOLDBACK = 'PURCHASE_DECISION_HOLDBACK'
    PURCHASE_DECISION_REQUEST = 'PURCHASE_DECISION_REQUEST'
    PURCHASE_DECISION_HOLDBACK_RELEASE = 'PURCHASE_DECISION_HOLDBACK_RELEASE'
    ADMIN_CANCELING = 'ADMIN_CANCELING'
    ADMIN_CANCEL_DONE = 'ADMIN_CANCEL_DONE'
    ADMIN_CANCEL_REJECT = 'ADMIN_CANCEL_REJECT'


class GiftReceivingStatus:
    """
    string (giftReceivingStatus.pay-order-seller)
    선물 수락 상태 구분. 250바이트 내외

    WAIT_FOR_RECEIVING	수락 대기(배송지 입력 대기)
    RECEIVED	수락 완료
    """
    WAIT_FOR_RECEIVING = 'WAIT_FOR_RECEIVING'
    RECEIVED = 'RECEIVED'


class LastChangeStatus(BaseModel):
    # id: int
    orderId: str
    productOrderId: str
    productOrderStatus: str
    paymentDate: datetime.datetime
    lastChangedDate: datetime.datetime
    lastChangedType: str
    receiverAddressChanged: bool

    class Config:
        orm_mode = True


class LastChangeStatusList(BaseModel):
    lastChangeStatus_list: list[LastChangeStatus]
