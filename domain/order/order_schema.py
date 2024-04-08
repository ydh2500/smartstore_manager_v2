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

    class Config:
        orm_mode = True