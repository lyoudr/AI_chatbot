from routes import chatbot
from settings import get_settings

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.middleware.gzip import GZipMiddleware  # noqa: E402
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

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

# Initialize Kafka producer and consumer globally
producer = None
consumer_task = None

@app.on_event("startup")
async def startup_event():
    global producer, consumer_task
    # Initialize producer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
    )
    await producer.start()
    # Start the Kafka consumer
    consumer_task = asyncio.create_task(consume())

@app.on_event("shutdown")
async def shutdown_event():
    global producer
    # Stop the Kafka producer
    await producer.stop()

    # Cancel the consumer task
    consumer_task.cancel()

@app.post("/send")
async def send_message(message: str):
    await producer.send_and_wait(
        settings.KAFKA_TOPIC, 
        message.encode("utf-8")
    )
    return {"status": "Message sent"}


async def consume():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="fastapi-consumer-group",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Consumed message: {msg.value.decode('utf-8')}")
    finally:
        await consumer.stop()