import asyncio
import aio_pika, json
from aio_pika import Message
from aggregator import Aggregator


async def main():
    # Подключаемся к RabbitMQ
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost:5672/")
    channel = await connection.channel()

    # Подписываемся на очередь запросов
    queue = await channel.declare_queue("api_aggregation_queue", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                # Берём тело и метаданные
                body = message.body
                correlation_id = message.correlation_id
                reply_to = message.reply_to
                data = json.loads(body.decode())

                if not reply_to or not correlation_id:
                    print("Пропущено сообщение без reply_to/correlation_id")
                    continue

                # Обрабатываем сообщение
                calculator = Aggregator(data)
                result = await calculator.calculate()

                # Отправляем результат в очередь reply_to
                await channel.default_exchange.publish(
                    Message(
                        body=json.dumps(result).encode('utf-8'),
                        correlation_id=correlation_id
                    ),
                    routing_key=reply_to
                )

                print(f"Ответ отправлен в {reply_to} с correlation_id {correlation_id}")


if __name__ == "__main__":
    asyncio.run(main())
