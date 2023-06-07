from typing import Annotated
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from tortoise.contrib.pydantic import pydantic_model_creator

from contract_watcher.dependencies import get_current_user
from contract_watcher.models import User, Webhook


class AbiParam(BaseModel):
    type: str
    name: str | None
    indexed: bool | None


class AbiEntry(BaseModel):
    type: str
    name: str | None
    inputs: list[AbiParam] | None
    outputs: list[AbiParam] | None
    stateMutability: str | None
    anonymous: bool | None


class CreateWebhookModel(
    pydantic_model_creator(
        Webhook,
        exclude=('id', 'active', 'user', 'history', 'abi'),
        name='CreateWebhookModel'
    )
):
    abi: list['AbiEntry']


WebhookModel = pydantic_model_creator(Webhook, exclude=('user', 'history', 'abi'), name='WebhookModel')


router = APIRouter(
    tags=['Webhooks'],
)


@router.post(
    '/webhooks',
    response_model=WebhookModel,
)
async def create_webhook(
        user: Annotated[User, Depends(get_current_user)],
        body: CreateWebhookModel
):
    webhook = await Webhook.create(**body.dict(exclude_unset=True), user=user)
    return await WebhookModel.from_tortoise_orm(webhook)


@router.get(
    '/webhooks',
    response_model=list[WebhookModel]
)
async def list_webhooks(user: Annotated[User, Depends(get_current_user)]):
    return await WebhookModel.from_queryset(user.webhooks.all())


@router.delete(
    '/webhooks/{wid}',
    response_model=WebhookModel,
)
async def delete_webhook(user: Annotated[User, Depends(get_current_user)], wid: int):
    webhook = await user.webhooks.all().get_or_none(id=wid)

    if webhook is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found"
        )

    webhookModel = await WebhookModel.from_tortoise_orm(webhook)

    await webhook.delete()

    return webhookModel.dict()
