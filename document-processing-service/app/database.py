from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings
from contextlib import contextmanager


engine = create_engine(
    settings.postgres_url,
    echo=True,
    pool_size=20,        # Увеличьте размер пула
    max_overflow=10,     # Максимальное количество дополнительных соединений
    pool_timeout=30,     # Время ожидания свободного соединения
    pool_recycle=3600    # Время в секундах до перераспределения соединения
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


