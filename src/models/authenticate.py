from pydantic import BaseModel 

class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
