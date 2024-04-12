from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.order import order_schema
from domain.order.order_schema import LastChangedType
from domain.order.order_utils import get_orders_for_days, get_order_details, confirm_orders

router = APIRouter(
    prefix="/api/order",
)


@router.get("/all_changed_list", response_model=order_schema.LastChangeStatusList)
def get_all_changed_list(since_from: datetime, db: Session = Depends(get_db)):
    all_changed_list = get_orders_for_days(since_from, None)
    return all_changed_list


@router.get("/pay_waiting_list", response_model=order_schema.LastChangeStatusList)
def get_pay_waiting_list(since_from: datetime, db: Session = Depends(get_db)):
    pay_waiting_list = get_orders_for_days(since_from, LastChangedType.PAY_WAITING)
    return pay_waiting_list


@router.get("/payed_list", response_model=order_schema.LastChangeStatusList)
def get_payed_list(since_from: datetime, db: Session = Depends(get_db)):
    payed_list = get_orders_for_days(since_from, LastChangedType.PAYED)
    return payed_list


@router.get("/purchase_decided_list", response_model=order_schema.LastChangeStatusList)
def get_purchase_decided_list(since_from: datetime, db: Session = Depends(get_db)):
    purchase_decided_list = get_orders_for_days(since_from, LastChangedType.PURCHASE_DECIDED)
    return purchase_decided_list


@router.get("/order_detail_list", response_model=order_schema.OrderDetails)
def get_order_detail_list(product_order_ids: List[str] = Query([]), db: Session = Depends(get_db)):
    order_details = get_order_details(product_order_ids)
    return order_details


# 발주 확인처리
@router.post("/order_confirm")
def order_confirm(product_order_ids: List[str] = Query([]), db: Session = Depends(get_db)):
    confirm_result = confirm_orders(product_order_ids)
    return confirm_result