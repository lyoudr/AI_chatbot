from sqlalchemy import (
    Column,
    VARCHAR,
    BigInteger,
    TEXT
)
from . import Base


class ChatBotLog(Base):
    __tablename__ = "chat_bot"

    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(VARCHAR(20))
    question = Column(TEXT)