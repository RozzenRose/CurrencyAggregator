import asyncio
from rabbitmq import consume_queue, RabbitMQConnectionManager


async def main():
    channel = await RabbitMQConnectionManager.get_channel()

    # Список очередей, на которые подписываемся
    queues = [
        "api_aggregation_queue",
        "report_aggregation_queue"
    ]

    # Запускаем слушателей параллельно
    await asyncio.gather(*(consume_queue(q, channel) for q in queues))


if __name__ == "__main__":
    asyncio.run(main())
