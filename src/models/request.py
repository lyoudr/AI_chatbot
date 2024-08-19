from pydantic import BaseModel
from typing import List 


class MultipleQuestionRequest(BaseModel):
    questions: List[str]