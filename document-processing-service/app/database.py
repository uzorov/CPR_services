from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings
from contextlib import contextmanager


engine = create_engine(
    settings.postgres_url,
    echo=True,
    pool_size=20,        
    max_overflow=10,     
    pool_timeout=30,    
    pool_recycle=3600    
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


