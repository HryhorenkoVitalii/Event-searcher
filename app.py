import json
from typing import Any, Optional, Union
from fastapi import Depends, FastAPI, Header
from loguru import logger
from config import ApiConfig
from controllers import api_router

config = ApiConfig()

api = FastAPI(
    title=config.title,
    docs_url=config.docs_url,
    openapi_url=config.openapi_url,
    redoc_url=config.redoc_url
)

def auth_check(authentication: Optional[str] = Header(default=None, alias='Authorization')) -> None:
    return
    # raise HTTPException(status.HTTP_401_UNAUTHORIZED)


api.include_router(
    router=api_router,
    prefix='/api',
    tags=['v0.1.0'],
    dependencies=[Depends(auth_check)],
    # responses=DefaultResponsesSample
)

