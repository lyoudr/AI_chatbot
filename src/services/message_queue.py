import aio_pika

from settings import get_settings

settings = get_settings()

async def publish_message(queue_name: str, message: str):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=queue.name
        )



