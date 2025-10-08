import asyncio
import aio_pika
import json
from aio_pika import Message
from aggregator import Aggregator
from config import settings


async def handle_message(message: aio_pika.IncomingMessage, channel: aio_pika.Channel):
    async with message.process():
        body = message.body
        correlation_id = message.correlation_id
        reply_to = message.reply_to

        if not reply_to or not correlation_id:
            print("Пропущено сообщение без reply_to/correlation_id")
            return

        data = json.loads(body.decode())

        calculator = Aggregator(data)
        result = await calculator.calculate()

        await channel.default_exchange.publish(
            Message(
                body=json.dumps(result).encode('utf-8'),
                correlation_id=correlation_id
            ),
            routing_key=reply_to
        )

        print(f"Ответ отправлен в {reply_to} с correlation_id {correlation_id}")


async def consume_queue(queue_name: str, channel: aio_pika.Channel):
    queue = await channel.declare_queue(queue_name, durable=True)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await handle_message(message, channel)


async def main():
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()

    # Список очередей, на которые подписываемся
    queues = [
        "api_aggregation_queue",
        "report_aggregation_queue"
    ]

    # Запускаем слушателей параллельно
    await asyncio.gather(*(consume_queue(q, channel) for q in queues))


if __name__ == "__main__":
    asyncio.run(main())
