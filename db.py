from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Database URLs
DATABASE_URL_SYNC = "sqlite:///./db.sqlite3" 
DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./db.sqlite3" 

# Create sync engine & session factory
sync_engine = create_engine(DATABASE_URL_SYNC, connect_args={"check_same_thread": False})
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Create async engine & session factory
async_engine = create_async_engine(DATABASE_URL_ASYNC, connect_args={"check_same_thread": False})
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)


# Base = declarative_base()

class Base(DeclarativeBase):
    pass

# for Sync Database Session
def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()  

# Async Database Session
async def get_async_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()  
