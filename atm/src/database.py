from os import environ
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


DATABASE_URL = "postgresql+asyncpg://" + environ.get("DATABASE_URL")


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = async_sessionmaker(
    engine, expire_on_commit=False
)

async def get_session():
    async with async_session() as session:
        yield session
