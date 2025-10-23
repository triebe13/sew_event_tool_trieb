from collections.abc import Generator
from typing import Annotated

from sqlalchemy.orm import Session

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.database.session import engine
from app.core import security
from app.core.config import settings

from app.schemas.token import TokenData
from app.schemas.user import User
from app.crud.user import get_user_by_email


# Database Session
def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a SQLAlchemy session.

    This function is a generator that yields a SQLAlchemy session object.
    It ensures that the session is properly closed after use.

    Yields:
        Session: A SQLAlchemy session object.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

# Security
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")

TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """
    Retrieve the current user based on the provided session and token.

    Args:
        session (SessionDep): The database session dependency.
        token (TokenDep): The JWT token dependency.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If the token is invalid, credentials cannot be validated,
                       the user is not found, or the user is inactive.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        token_data = TokenData(username=username)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    assert token_data.username is not None
    user = get_user_by_email(db=session, email=token_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user.updated_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    """
    Verify if the current user is a superuser.

    Args:
        current_user (CurrentUser): The user object to be checked.

    Returns:
        User: The current user if they are a superuser.

    Raises:
        HTTPException: If the current user is not a superuser, an HTTP 403 Forbidden exception is raised.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
