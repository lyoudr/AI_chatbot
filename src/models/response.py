from pydantic import BaseModel 

class SendTaskResponse(BaseModel):
    status: str 

class ReceiveTaskResponse(BaseModel):
    status: str 