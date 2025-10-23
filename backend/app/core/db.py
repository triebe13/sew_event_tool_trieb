from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import settings

from app.database.session import Base, engine
from app.schemas import user as schemas
from app.crud import user as crud

# models must be imported and registered from app.models to create the tables
from app.models.user import User


def init_db(session: Session) -> None:
    """
    Initialize the database by creating tables and a superuser if it doesn't exist.

    Args:
      session (Session): The database session used to interact with the database.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create superuser
    superuser = session.execute(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    ).first()
    if not superuser:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        _ = crud.create_superuser(db=session, user=user_in)
