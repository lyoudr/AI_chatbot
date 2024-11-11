# flaske8: noqa
import psycopg2
import subprocess
import sys

sys.path.append("src")
import os 
from settings import Settings
from sqlalchemy_utils import (
    database_exists, 
    create_database, 
    drop_database
)

settings = Settings()

def create_test_db() -> None:
    db_name = settings.TEST_DB_NAME

    # PostgreSQL connection URL for SQLAlchemy URL
    sqlalchemy_url = f"postgresql+psycopg2://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{db_name}"

    if database_exists(sqlalchemy_url):
        drop_database(sqlalchemy_url)
    create_database(sqlalchemy_url, encoding="utf8")

    # Set environment variable for testing
    os.environ["APP_ENV"] = "testing"

    # Run alembic migrations for main database
    subprocess.call(["alembic", "upgrade", "head"])
    print("Test database cloud center initialization completed.")

# Call the function to create the test databases
create_test_db()