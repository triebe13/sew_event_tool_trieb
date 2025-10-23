from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.main import api_router

from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

from app.database.session import Base, engine




def cstm_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_prefix=f"{settings.API_V1_STR}",
    # openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=cstm_generate_unique_id,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)



# models must be imported and registered from app.models to create the tables

# Create tables
#Base.metadata.create_all(bind=engine)
