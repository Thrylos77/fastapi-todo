from typing import Annotated
from fastapi import APIRouter, Request, Depends
from starlette import status
from . import model
from . import service
from fastapi.security import OAuth2PasswordRequestForm
from ..db.core import DbSession
from ..core.rate_limiting import limiter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/hour")
async def register_user(request: Request, db: DbSession, 
                        register_user_request: model.RegisterUserRequest):
    service.register_user(db, register_user_request)


@router.post("/token", response_model=model.Token)
async def login_for_access_token(db: DbSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return service.login_for_access_token(db, form_data)