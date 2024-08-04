from pydantic import BaseModel

class ChatBotResponse(BaseModel):
    status: str