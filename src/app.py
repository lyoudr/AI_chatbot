from routes import chatbot, authenticate, tasks
from settings import get_settings

from aio_pika import connect, IncomingMessage, ExchangeType
from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.middleware.gzip import GZipMiddleware  # noqa: E402
from contextlib import asynccontextmanager
import asyncio

settings = get_settings()

app = FastAPI(
    title=f"FastAPI - {settings.APP_ENV}",
    docs_url="/docs" if settings.DOCS else None,
    description="FastAPI Documentation",
    version=settings.APP_VERSION,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "tryItOutEnabled": True,
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "X-Internal-User-Email"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)
# include router
app.include_router(chatbot.router)
app.include_router(authenticate.router)
app.include_router(tasks.router)



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
        queue = await channel.declare_exchange("task_queue", durable=True)

        # Step 4: Bind the queue to the exchange
        await queue.bind(exchange, routing_key="task_key")

        # Step 5: Consume messages from the queue
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await process_message(message) # Process each incoming message


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start consumer in a background task
    consumer_task = asyncio.create_task(start_consumer())
    yield # This allows the app to run while `start_consumer`
    consumer_task.cancel() # Cancel the consumer task on shutdown


app.router.lifespan_context = lifespan