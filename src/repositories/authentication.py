from sqlalchemy.orm import Session
from fastapi import status

from db_models.user import User
from utils.errors import CustomException
from database import get_db_session


def batch_insert(data: list):
    db = next(get_db_session())
    db.bulk_insert_mappings(User, data)
    db.commit()


def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise CustomException(
            error_code=status.HTTP_404_NOT_FOUND,
            error_msg=f'Can not find user: {username}'
        )
    return user