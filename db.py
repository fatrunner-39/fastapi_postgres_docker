import asyncio
import os

import databases
from sqlalchemy import create_engine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from dotenv import load_dotenv
from contextlib import contextmanager, asynccontextmanager

load_dotenv()


Base = declarative_base()

DATABASE_URL = f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}" \
               f"@{os.environ.get('POSTGRES_SERVER')}:{os.environ.get('POSTGRES_PORT')}/" \
               f"{os.environ.get('POSTGRES_DB')}"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

sa_engine = create_engine(DATABASE_URL)

sa_factory = sessionmaker(autocommit=False, autoflush=False, bind=sa_engine)

@contextmanager
def get_db_session():
    with sa_engine.connect() as conn:
        session = sa_factory(bind=conn)
        try:
            yield session
        except Exception:
            raise
        finally:
            session.close()



    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)
    #
    # # expire_on_commit=False will prevent attributes from being expired
    # # after commit.
    # async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    #
    # await engine.dispose()
