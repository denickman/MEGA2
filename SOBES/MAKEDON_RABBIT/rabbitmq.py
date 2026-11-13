import asyncio
import json

import aio_pika
from aio_pika import ExchangeType
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue


'''
Ты → Exchange → (по правилу routing key) → Queue → Consumer забирает

Ты (producer) никогда не относишь письмо напрямую в ящик (очередь).
Ты всегда относишь письмо в сортировочный центр (exchange), и уже центр, по правилам (bindings), 
сам решает, в какой ящик (очередь) его положить.


exchange = "orders"                     # сортировочный центр "Заказы"
это не ящик и не хранилище. Он ничего не хранит, он просто мгновенно решает "куда разложить" и передаёт дальше. 
Сам exchange письма не держит.

это как сортировочный центр на почте. Ты не кидаешь письмо прямо в конкретный ящик получателя — ты отдаёшь 
его в сортировочный центр с пометкой ("для заказов", "срочное" и т.п.), а центр уже решает, 
в какие ящики (очереди) это письмо разложить, по правилам (routing key).

queue = "notifications.order_created"   # ящик для уведомлений


routing_key = "order.created"            # метка на письме "заказ создан"
Routing key — это как индекс/адрес на письме, по которому сортировочный центр понимает, куда направить.
'''


NOTIFICATION_QUEUE = "notifications.order_created"
ORDER_EXCHANGE = "orders"
ORDER_ROUTING_KEY = "order.created"


async def connect_rabbitmq():
    return await aio_pika.connect_robust("amqp://guest:guest@localhost:5672/")


async def declare_orders_exchange(channel: AbstractChannel) -> AbstractExchange:
    return await channel.declare_exchange(ORDER_EXCHANGE, ExchangeType.DIRECT)


async def declare_notifications_queue(
    channel: AbstractChannel,
    exchange: AbstractExchange
) -> AbstractQueue:
    queue: AbstractQueue = await channel.declare_queue(NOTIFICATION_QUEUE)
    await queue.bind(exchange, routing_key=ORDER_ROUTING_KEY)
    return queue



async def publish_json(exchange: AbstractExchange, routing_key: str, data: dict):
    message = aio_pika.Message(json.dumps(data).encode())
    await exchange.publish(message, routing_key=routing_key)











