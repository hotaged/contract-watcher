from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contract_watcher.config import settings, TORTOISE_ORM
from contract_watcher import routers

from tortoise import Tortoise


app = FastAPI(
    title='Contract Watcher API',
    version='1.0.0'
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers
)

for router in routers.members:
    app.include_router(router, prefix='/api')


if settings.debug:
    from contract_watcher.routers.debug import router
    app.include_router(router)


@app.on_event('startup')
async def init_orm():
    await Tortoise.init(TORTOISE_ORM)

