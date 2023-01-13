import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from contextlib import contextmanager

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

