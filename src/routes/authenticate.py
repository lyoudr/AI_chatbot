import sys
sys.path.append("src")

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm  import Session
from typing import Annotated
from datetime import timedelta

from models.authenticate import Token
from utils.authenticate import authenticate_user, create_access_token
from utils.errors import CustomException
from database import get_db_session


ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter(prefix="")


@router.post(
    "/token",
    tags = ["auth"],
    summary = "log in user",
    response_model=Token
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db_session)
) -> Token:
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise CustomException(
            error_code=status.HTTP_401_UNAUTHORIZED,
            error_msg=f"User {form_data.username} is not authenticated."
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")