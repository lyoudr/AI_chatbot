from pydantic import BaseModel
from typing import List 


class MultipleQuestionRequest(BaseModel):
    question: str


class RAGLLMQuestionRequest(BaseModel):
    question: str