import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database.session import Base
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.main import app
from datetime import datetime
from passlib.context import CryptContext

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
ALGORITHM = "HS256"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@pytest.fixture(scope="function")
def db():
    """Creates a new database session and ensures tables exist."""
    Base.metadata.create_all(bind=engine)  
    session = TestingSessionLocal()
    try:
        yield session  
    finally:
        session.rollback()
        session.close()
        #Base.metadata.drop_all(bind=engine)  

@pytest.fixture(scope="function")
def client(db):
    """Provides a FastAPI test client using the same session as the test."""
    
    def override_get_db():
        Base.metadata.create_all(bind=engine) 
        yield db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def test_superuser(db):
    """Creates a superuser in the test database."""
    user = User(username="superuser", email="superuser@example.com", hashed_password=hash_password("Kennwort1"), is_superuser=True, created_at=datetime.now())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def client_with_superuser(client, test_superuser):
    """Override `get_current_active_superuser` to return an admin user."""
    def override_get_current_user():
        return test_superuser  
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    return client



