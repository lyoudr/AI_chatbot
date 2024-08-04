from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import get_settings, is_testing
import time

settings = get_settings()

db_user = settings.DB_USERNAME
db_pass = settings.DB_PASSWORD
db_host = settings.DB_HOST
db_port = settings.DB_PORT

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_port}"
)


# @event.listens_for(Engine, "before_cursor_execute")
# def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     conn.info.setdefault('query_start_time', []).append(time.time())


# @event.listens_for(Engine, "after_cursor_execute")
# def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     total = time.time() - conn.info['query_start_time'].pop(-1)
#     print(f"Query:{statement}")
#     print(f"Execution time: {total} seconds")


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600,
    pool_size=30
)
load_data_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600,
    pool_size=30,
    connect_args={"local_infile": True},
)
read_uncommited_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    isolation_level="READ UNCOMMITTED",
    pool_recycle=3600,
    pool_size=20,
)

_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_sqlalchemy_db_url():
    return SQLALCHEMY_DATABASE_URL


def get_db_session():
    db = _Session()
    try:
        yield db
    finally:
        db.close()


