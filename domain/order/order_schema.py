import datetime

from pydantic import BaseModel, validator


class LastChangeStatuses(BaseModel):
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