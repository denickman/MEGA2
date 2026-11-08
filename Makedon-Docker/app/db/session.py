
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import get_settings


# просмотр таблиц - docker exec -it b9897c1e5892 psql -U postgres -d postgres -c "\dt"


settings = get_settings()
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker[Session](bind=engine)




def get_db():
    '''
    method for dep inejection of data base
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()