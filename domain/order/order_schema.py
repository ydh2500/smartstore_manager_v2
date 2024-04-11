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


class OrderDetails(BaseModel):
    """
    example
    {
      "timestamp": "2023-01-16T17:14:51.794+09:00",
      "traceId": "string",
      "data": [
        {
          "cancel": {
            "cancelApprovalDate": "2023-01-16T17:14:51.794+09:00",
            "cancelCompletedDate": "2023-01-16T17:14:51.794+09:00",
            "cancelDetailedReason": "string",
            "cancelReason": "string",
            "claimRequestDate": "2023-01-16T17:14:51.794+09:00",
            "claimStatus": "string",
            "refundExpectedDate": "2023-01-16T17:14:51.794+09:00",
            "refundStandbyReason": "string",
            "refundStandbyStatus": "string",
            "requestChannel": "string"
          },
          "delivery": {
            "deliveredDate": "2023-01-16T17:14:51.794+09:00",
            "deliveryCompany": "string",
            "deliveryMethod": "DELIVERY",
            "deliveryStatus": "COLLECT_REQUEST",
            "isWrongTrackingNumber": true,
            "pickupDate": "2023-01-16T17:14:51.794+09:00",
            "sendDate": "2023-01-16T17:14:51.794+09:00",
            "trackingNumber": "string",
            "wrongTrackingNumberRegisteredDate": "2023-01-16T17:14:51.794+09:00",
            "wrongTrackingNumberType": "string"
          },
          "exchange": {
            "claimDeliveryFeeDemandAmount": 0,
            "claimDeliveryFeePayMeans": "string",
            "claimDeliveryFeePayMethod": "string",
            "claimRequestDate": "2023-01-16T17:14:51.794+09:00",
            "claimStatus": "string",
            "collectAddress": {
              "addressType": "string",
              "baseAddress": "string",
              "city": "string",
              "country": "string",
              "detailedAddress": "string",
              "name": "string",
              "state": "string",
              "tel1": "string",
              "tel2": "string",
              "zipCode": "string",
              "isRoadNameAddress": true
            },
            "collectCompletedDate": "2023-01-16T17:14:51.794+09:00",
            "collectDeliveryCompany": "string",
            "collectDeliveryMethod": "DELIVERY",
            "collectStatus": "NOT_REQUESTED",
            "collectTrackingNumber": "string",
            "etcFeeDemandAmount": 0,
            "etcFeePayMeans": "string",
            "etcFeePayMethod": "string",
            "exchangeDetailedReason": "string",
            "exchangeReason": "string",
            "holdbackDetailedReason": "string",
            "holdbackReason": "string",
            "holdbackStatus": "string",
            "reDeliveryMethod": "DELIVERY",
            "reDeliveryStatus": "COLLECT_REQUEST",
            "reDeliveryCompany": "string",
            "reDeliveryTrackingNumber": "string",
            "requestChannel": "string",
            "returnReceiveAddress": {
              "addressType": "string",
              "baseAddress": "string",
              "city": "string",
              "country": "string",
              "detailedAddress": "string",
              "name": "string",
              "state": "string",
              "tel1": "string",
              "tel2": "string",
              "zipCode": "string",
              "isRoadNameAddress": true
            },
            "holdbackConfigDate": "2023-01-16T17:14:51.794+09:00",
            "holdbackConfigurer": "string",
            "holdbackReleaseDate": "2023-01-16T17:14:51.794+09:00",
            "holdbackReleaser": "string",
            "claimDeliveryFeeProductOrderIds": "string",
            "reDeliveryOperationDate": "2023-01-16T17:14:51.794+09:00",
            "claimDeliveryFeeDiscountAmount": 0,
            "remoteAreaCostChargeAmount": 0
          },
          "order": {
            "chargeAmountPaymentAmount": 0,
            "checkoutAccumulationPaymentAmount": 0,
            "generalPaymentAmount": 0,
            "naverMileagePaymentAmount": 0,
            "orderDate": "2023-01-16T17:14:51.794+09:00",
            "orderDiscountAmount": 0,
            "orderId": "string",
            "ordererId": "string",
            "ordererName": "string",
            "ordererTel": "string",
            "paymentDate": "2023-01-16T17:14:51.794+09:00",
            "paymentDueDate": "2023-01-16T17:14:51.794+09:00",
            "paymentMeans": "string",
            "isDeliveryMemoParticularInput": "string",
            "payLocationType": "string",
            "ordererNo": "string",
            "payLaterPaymentAmount": 0
          },
          "productOrder": {
            "claimStatus": "string",
            "claimType": "string",
            "decisionDate": "2023-01-16T17:14:51.794+09:00",
            "delayedDispatchDetailedReason": "string",
            "delayedDispatchReason": "PRODUCT_PREPARE",
            "deliveryDiscountAmount": 0,
            "deliveryFeeAmount": 0,
            "deliveryPolicyType": "string",
            "expectedDeliveryMethod": "DELIVERY",
            "freeGift": "string",
            "mallId": "string",
            "optionCode": "string",
            "optionPrice": 0,
            "packageNumber": "string",
            "placeOrderDate": "2023-01-16T17:14:51.794+09:00",
            "placeOrderStatus": "string",
            "productClass": "string",
            "productDiscountAmount": 0,
            "productId": "string",
            "originalProductId": "string",
            "merchantChannelId": "string",
            "productName": "string",
            "productOption": "string",
            "productOrderId": "string",
            "productOrderStatus": "string",
            "quantity": 0,
            "sectionDeliveryFee": 0,
            "sellerProductCode": "string",
            "shippingAddress": {
              "addressType": "string",
              "baseAddress": "string",
              "city": "string",
              "country": "string",
              "detailedAddress": "string",
              "name": "string",
              "state": "string",
              "tel1": "string",
              "tel2": "string",
              "zipCode": "string",
              "isRoadNameAddress": true,
              "pickupLocationType": "FRONT_OF_DOOR",
              "pickupLocationContent": "string",
              "entryMethod": "LOBBY_PW",
              "entryMethodContent": "string"
            },
            "shippingStartDate": "2023-01-16T17:14:51.794+09:00",
            "shippingDueDate": "2023-01-16T17:14:51.794+09:00",
            "shippingFeeType": "string",
            "shippingMemo": "string",
            "takingAddress": {
              "addressType": "string",
              "baseAddress": "string",
              "city": "string",
              "country": "string",
              "detailedAddress": "string",
              "name": "string",
              "state": "string",
              "tel1": "string",
              "tel2": "string",
              "zipCode": "string",
              "isRoadNameAddress": true
            },
            "totalPaymentAmount": 0,
            "totalProductAmount": 0,
            "unitPrice": 0,
            "sellerBurdenDiscountAmount": 0,
            "commissionRatingType": "string",
            "commissionPrePayStatus": "string",
            "paymentCommission": 0,
            "saleCommission": 0,
            "expectedSettlementAmount": 0,
            "inflowPath": "string",
            "inflowPathAdd": "string",
            "itemNo": "string",
            "optionManageCode": "string",
            "sellerCustomCode1": "string",
            "sellerCustomCode2": "string",
            "claimId": "string",
            "channelCommission": 0,
            "individualCustomUniqueCode": "string",
            "productImediateDiscountAmount": 0,
            "productProductDiscountAmount": 0,
            "productMultiplePurchaseDiscountAmount": 0,
            "sellerBurdenImediateDiscountAmount": 0,
            "sellerBurdenProductDiscountAmount": 0,
            "sellerBurdenMultiplePurchaseDiscountAmount": 0,
            "knowledgeShoppingSellingInterlockCommission": 0,
            "giftReceivingStatus": "string",
            "sellerBurdenStoreDiscountAmount": 0,
            "sellerBurdenMultiplePurchaseDiscountType": "IGNORE_QUANTITY",
            "logisticsCompanyId": "string",
            "logisticsCenterId": "string",
            "hopeDelivery": {
              "region": "string",
              "additionalFee": 0,
              "hopeDeliveryYmd": "string",
              "hopeDeliveryHm": "string",
              "changeReason": "string",
              "changer": "string"
            },
            "arrivalGuaranteeDate": "2023-01-16T17:14:51.794+09:00",
            "deliveryAttributeType": "NORMAL"
          },
          "return": {
            "claimDeliveryFeeDemandAmount": 0,
            "claimDeliveryFeePayMeans": "string",
            "claimDeliveryFeePayMethod": "string",
            "claimRequestDate": "2023-01-16T17:14:51.794+09:00",
            "claimStatus": "string",
            "collectAddress": {
              "addressType": "string",
              "baseAddress": "string",
              "city": "string",
              "country": "string",
              "detailedAddress": "string",
              "name": "string",
              "state": "string",
              "tel1": "string",
              "tel2": "string",
              "zipCode": "string",
              "isRoadNameAddress": true
            },
            "collectCompletedDate": "2023-01-16T17:14:51.794+09:00",
            "collectDeliveryCompany": "string",
            "collectDeliveryMethod": "DELIVERY",
            "collectStatus": "NOT_REQUESTED",
            "collectTrackingNumber": "string",
            "etcFeeDemandAmount": 0,
            "etcFeePayMeans": "string",
            "etcFeePayMethod": "string",
            "holdbackDetailedReason": "string",
            "holdbackReason": "string",
            "holdbackStatus": "string",
            "refundExpectedDate": "2023-01-16T17:14:51.794+09:00",
            "refundStandbyReason": "string",
            "refundStandbyStatus": "string",
            "requestChannel": "string",
            "returnDetailedReason": "string",
            "returnReason": "string",
            "returnReceiveAddress": {
              "addressType": "string",
              "baseAddress": "string",
              "city": "string",
              "country": "string",
              "detailedAddress": "string",
              "name": "string",
              "state": "string",
              "tel1": "string",
              "tel2": "string",
              "zipCode": "string",
              "isRoadNameAddress": true
            },
            "returnCompletedDate": "2023-01-16T17:14:51.794+09:00",
            "holdbackConfigDate": "2023-01-16T17:14:51.794+09:00",
            "holdbackConfigurer": "string",
            "holdbackReleaseDate": "2023-01-16T17:14:51.794+09:00",
            "holdbackReleaser": "string",
            "claimDeliveryFeeProductOrderIds": "string",
            "claimDeliveryFeeDiscountAmount": 0,
            "remoteAreaCostChargeAmount": 0
          }
        }
      ]
    }
    """
    timestamp: datetime.datetime
    traceId: str
    data: list[dict]
