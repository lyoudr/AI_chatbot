from pydantic import BaseModel 

class SendTaskResponse(BaseModel):
    status: str 