from typing import Annotated

from fastapi import APIRouter, Depends
from tortoise.contrib.pydantic import pydantic_model_creator

from contract_watcher.dependencies import get_current_user
from contract_watcher.models import User, History


router = APIRouter(
    tags=['History']
)


HistoryModel = pydantic_model_creator(History)


@router.get('/history', response_model=list[HistoryModel])
async def get_history(user: Annotated[User, Depends(get_current_user)]):
    history = await HistoryModel.from_queryset(user.history.all())
    return history
