from pydantic import BaseModel


class ChatBotResponse(BaseModel):
    status: str


class RAGLLMResponse(BaseModel):
    response: str