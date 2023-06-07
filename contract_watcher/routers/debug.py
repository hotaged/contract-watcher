from fastapi import APIRouter

router = APIRouter(
    tags=['Debug']
)


@router.post('/event')
async def debug_event(body: dict):
    print(body)
    return {'status': 'OK'}
