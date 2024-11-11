from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import get_settings, is_testing

settings = get_settings()

db_user = settings.DB_USERNAME
db_pass = settings.DB_PASSWORD
db_host = settings.DB_HOST
db_port = settings.DB_PORT
db_name = settings.TEST_DB_NAME if is_testing() else settings.DB_NAME

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600,
    pool_size=30
)

_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db_session():
    db = _Session()
    try:
        yield db
    finally:
        db.close()