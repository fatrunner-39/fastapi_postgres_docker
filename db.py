import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


Base = declarative_base()

DATABASE_URL = (
    f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
    f"@{os.environ.get('POSTGRES_SERVER')}:{os.environ.get('POSTGRES_PORT')}/"
    f"{os.environ.get('POSTGRES_DB')}"
)

SYNC_DATABASE_URL = (
    f"postgresql+psycopg2://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
    f"@{os.environ.get('POSTGRES_SERVER')}:{os.environ.get('POSTGRES_PORT')}/"
    f"{os.environ.get('POSTGRES_DB')}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

sync_engine = create_engine(SYNC_DATABASE_URL)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

sa_factory = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


@contextmanager
def get_db_session():
    with sync_engine.connect() as conn:
        session = sa_factory(bind=conn)
        try:
            yield session
        except Exception:
            raise
        finally:
            session.close()
