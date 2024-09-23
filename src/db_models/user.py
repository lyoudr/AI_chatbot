from sqlalchemy import (
    Column,
    VARCHAR,
    TEXT,
    BigInteger,
)
from . import Base

class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, nullable=False)
    username = Column(VARCHAR(30), nullable=False)
    email = Column(VARCHAR(100), nullable=False)
    hashed_password = Column(TEXT, nullable=False)