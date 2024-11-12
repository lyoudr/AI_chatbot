from sqlalchemy import Table, MetaData, text, create_engine
from sqlalchemy.orm import Session, sessionmaker

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
print("db url is ->", SQLALCHEMY_DATABASE_URL)

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


def truncate_table(
    table: str, 
    alter_auto_increment: bool = False,
    db: Session = None 
):
    if db is None:
        db = next(get_db_session())
        
    metadata = MetaData()
    
    # Use `autoload_with=engine` to load table schema from the database
    table = Table(table, metadata, autoload_with=engine)

    # Use `table.delete()` for PostgreSQL
    db.execute(table.delete())  # Equivalent to TRUNCATE for PostgreSQL
    if alter_auto_increment:
        # PostgreSQL does not use AUTO_INCREMENT, but we can reset the serial column
        db.execute(text(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1"))
    
    db.commit()
