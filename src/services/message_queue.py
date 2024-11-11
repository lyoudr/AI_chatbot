from aio_pika import connect, IncomingMessage, ExchangeType
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


async def process_message(message: IncomingMessage):
    async with message.process():
        print("Received message:", message.body.decode())


async def start_consumer():
    # Step 1: Connect to RabbitMQ server
    connection = await connect(settings.RABBITMQ_URL)
    async with connection:
        # Step 2: Create a channel
        channel = await connection.channel()

        # Step 3: Declare the queue you want to consume from
        exchange = await channel.declare_exchange("task_exchange", ExchangeType.DIRECT, durable=True)
        queue = await channel.declare_queue("task_queue", durable=True)

        # Step 4: Bind the queue to the exchange
        await queue.bind(exchange, routing_key="task_key")

        # Step 5: Consume messages from the queue
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await process_message(message) # Process each incoming message


