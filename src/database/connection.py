from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)

from src.config import settings
from src.database.models import Base

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False
)

async_session_maker = async_sessionmaker(
    bind=engine,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False
)


@asynccontextmanager
async def get_context_session():
    async with async_session_maker() as session:
        yield session


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def populate() -> None:
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
        print("Successful populated")
