import asyncio
import json

from aio_pika.abc import AbstractIncomingMessage

from rabbitmq import connect_rabbitmq, declare_orders_exchange, declare_notifications_queue



async def handle_order_created(message: AbstractIncomingMessage):
   event_data = json.loads(message.body.decode())
   # имитация отправки уведомления на почту через celery
   # имитация сохранения в бд
   print(f'===RECEIVED MESSAGE: {event_data}')

   await message.ack()



async def main():
    connection = await connect_rabbitmq()
    channel = await connection.channel()
    orders_exchange = await declare_orders_exchange(channel)
    queue = await declare_notifications_queue(channel, orders_exchange)

    await queue.consume(handle_order_created)

    print("Ожидаю сообщения. Для выхода нажми CTRL+C")
    await asyncio.Future()  # держит программу живой вечно, пока не прервут

    await connection.close()



if __name__ == '__main__':
        asyncio.run(main())

