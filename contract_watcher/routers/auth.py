from typing import Annotated
from jose import jwt

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


from pydantic import BaseModel

from starlette import status

from datetime import datetime, timedelta

from contract_watcher.models import User
from contract_watcher.config import settings


router = APIRouter(
    tags=['Auth'],
    prefix='/auth'
)


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post('/token', response_model=Token)
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await User.get_or_none(username=form_data.username)

    if user is None or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = datetime.utcnow() + timedelta(seconds=settings.access_token_expires_seconds)

    encoded_key = jwt.encode(
        {"sub": str(user.id), "exp": access_token_expires},
        settings.secret_key, algorithm=settings.jwt_algorithm
    )

    return Token(access_token=encoded_key, token_type="bearer").dict()

