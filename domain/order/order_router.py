from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.order import order_schema
from domain.order.order_schema import LastChangedType
from naver_api import order_manager

router = APIRouter(
    prefix="/api/order",
)


@router.get("/pay_waiting_list", response_model=order_schema.LastChangeStatusList)
def get_pay_waiting_list(since_from: datetime, db: Session = Depends(get_db)):
    pay_waiting_list = order_manager.get_changed_orders(since_from, LastChangedType.PAY_WAITING)
    return pay_waiting_list