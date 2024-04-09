from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.order import order_schema
from domain.order.order_manager import NaverOrderManager
from domain.order.order_schema import LastChangedType

router = APIRouter(
    prefix="/api/order",
)

@router.get("/all_changed_list", response_model=order_schema.LastChangeStatusList)
def get_all_changed_list(since_from: datetime, db: Session = Depends(get_db)):
    order_manager = NaverOrderManager()
    all_changed_list = order_manager.get_orders_for_days(since_from, last_changed_type=None)
    return all_changed_list

@router.get("/pay_waiting_list", response_model=order_schema.LastChangeStatusList)
def get_pay_waiting_list(since_from: datetime, db: Session = Depends(get_db)):
    order_manager = NaverOrderManager()
    pay_waiting_list = order_manager.get_orders_for_days(since_from, LastChangedType.PAY_WAITING)
    return pay_waiting_list


@router.get("/payed_list", response_model=order_schema.LastChangeStatusList)
def get_payed_list(since_from: datetime, db: Session = Depends(get_db)):
    order_manager = NaverOrderManager()
    payed_list = order_manager.get_orders_for_days(since_from, LastChangedType.PAYED)
    return payed_list


@router.get("/purchase_decided_list", response_model=order_schema.LastChangeStatusList)
def get_purchase_decided_list(since_from: datetime, db: Session = Depends(get_db)):
    order_manager = NaverOrderManager()
    purchase_decided_list = order_manager.get_orders_for_days(since_from, LastChangedType.PURCHASE_DECIDED)
    return purchase_decided_list
