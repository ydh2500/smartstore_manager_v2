import traceback
from datetime import datetime, timedelta
import http.client
from auth.token_manager import get_token
from domain.order import order_router
from domain.order.order_manager import NaverOrderManager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.order.order_schema import LastChangedType
from naver_api import order_manager

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",  # Svelte
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_router.router)
# app.include_router(question_router.router)
# app.include_router(answer_router.router)
# app.include_router(user_router.router)
# app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

@app.get("/")
def index():
    return "Hello, World!"

# if __name__ == '__main__':
#
#     since_from_datetime = datetime.now() - timedelta(days=3)
#
#     try:
#         new_orders = order_manager.get_changed_orders(since_from_datetime)
#         print('New Orders:', new_orders)
#
#         new_orders = order_manager.get_orders_for_days(days=7, last_changed_type=LastChangedType.PAYED)
#         print('Weekly Orders:', new_orders)
#         # order_manager.confirm_orders(new_orders)
#     except Exception as e:
#         print(f'Order Error: {e}')
#         traceback.print_exc()