from fastapi import BackgroundTasks
from fastapi import APIRouter

from services.message_queue import (
    publish_message,
    start_consumer,
)
from models.response import (
    SendTaskResponse,
    ReceiveTaskResponse
)

router = APIRouter(prefix="/tasks")

@router.post(
    "/send_task"
)
async def send_task(
    message: str, 
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        publish_message,
        "task_queue",
        message
    )
    return SendTaskResponse(status = "Create task successfully.")

@router.get(
    "/get_message"
)
async def start_consumer_route():
    await start_consumer()
    return ReceiveTaskResponse(
        status = "Receive message successfully."
    )
