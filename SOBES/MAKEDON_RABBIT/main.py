from contextlib import asynccontextmanager
from uuid import uuid4
from pydantic import BaseModel
from fastapi import FastAPI, Request
from rabbitmq import connect_rabbitmq, declare_orders_exchange, publish_json, ORDER_ROUTING_KEY

class Product(BaseModel):
    name: str
    price: int

class Order(BaseModel):
    user_id: int
    products: list[Product]


'''
lifespan — это функция, которую FastAPI вызывает один раз при запуске сервера. Она должна:

Выполнить код до yield — это startup-логика.
"Заморозиться" на yield — всё это время приложение обслуживает запросы.
Когда сервер останавливают (Ctrl+C, graceful shutdown), выполнение продолжается после yield — это shutdown-логика.
'''

@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = await connect_rabbitmq()
    channel = await connection.channel()
    order_exchange = await declare_orders_exchange(channel)

    app.state.orders_exchange = order_exchange

    app.state.connection = connection
    app.state.channel = channel
    app.state.order_exchange = order_exchange

    yield

    await connection.close()


app = FastAPI(lifespan=lifespan)


@app.post('/orders')
async def create_order(payload: Order, request: Request):

    # save to db

    event_data = {
        'event_id': str(uuid4()),
        'event': 'order_created',
        'user_id': payload.user_id,
        'products': [product.model_dump() for product in payload.products],
    }

    await publish_json(exchange=request.app.state.order_exchange, routing_key=ORDER_ROUTING_KEY, data=event_data)

    return 'success mazafaka'
















