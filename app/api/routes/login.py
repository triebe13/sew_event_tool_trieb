from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.crud import user as crud
from app.schemas import token as schemas
from app.schemas.user import User
from app.api.deps import SessionDep, CurrentUser
from app.core.config import settings
from app.core import security


router = APIRouter(tags=["login"])


@router.post("/login", response_model=schemas.Token)
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> schemas.Token:
    user = crud.authenticate_user(
        db=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    elif user.updated_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return schemas.Token(
        access_token=security.create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )


@router.post("/me", response_model=User)
def test_access_token(current_user: CurrentUser) -> Any:
    return current_user
