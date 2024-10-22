import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from seazone.models.models import table_registry  # Importe seu modelo base

DATABASE_URL = 'sqlite+aiosqlite:///./test.db'


@pytest_asyncio.fixture(scope='session')
async def engine():
    engine = create_async_engine(DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def async_session_maker(engine):
    async_session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    yield async_session_maker


@pytest_asyncio.fixture
async def async_session(async_session_maker):
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def setup_and_teardown_db(engine):
    # Cria as tabelas antes dos testes
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)
    yield async_session_maker
    # Remove as tabelas após os testes
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)
