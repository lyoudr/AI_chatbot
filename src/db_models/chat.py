from sqlalchemy import (
    Column,
    VARCHAR,
    BigInteger,
)
from . import Base


class ChatBotLog(Base):
    __tablename__ = "chat_bot"

    id = Column(BigInteger, nullable=False)
    name = Column(VARCHAR(20))