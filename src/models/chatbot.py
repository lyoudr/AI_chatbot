from pydantic import BaseModel


class ChatBotResponse(BaseModel):
    status: str


class RAGLLMResponse(BaseModel):
    response: str


class MultipleResponse(BaseModel):
    status: str


class MultiTasksResponse(BaseModel):
    status: str