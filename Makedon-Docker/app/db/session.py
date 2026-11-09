from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

# просмотр таблиц - docker exec -it tasks-postgres psql -U postgres -d postgres -c "\dt"

settings = get_settings()

# echo управляется через SQL_ECHO=1, иначе SQL-лог забивает вывод
# и в нём не видно логов кэша.
engine = create_engine(settings.database_url, echo=settings.sql_echo, pool_pre_ping=True)

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
