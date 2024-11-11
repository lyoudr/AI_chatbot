import os
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseSettings


mode = os.getenv("MODE", "local")


class Settings(BaseSettings):
    APP_ENV: str = mode
    APP_VERSION: str = "0.0.0"
    SECRET_KEY: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = None
    TEST_DB_NAME: str = None
    DB_USERNAME: str = None
    DB_PASSWORD: str = None
    DOCS: bool = True
    GCP_PROJECT_ID: str
    GCS_BUCKET_NAME: str
    SELF_HOST: str
    REGION: str
    INDEX_ENDPOINT_NAME: str
    DEPLOYED_INDEX_ID: str
    PROCESSOR_ID: str
    PROCESSOR_VERSION_ID: str
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "bootstrap.test-cluster.us-central1.managedkafka.ann-project-390401.cloud.goog:9092"
    KAFKA_TOPIC: str = "example-topic"
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"

    class Config:
        env_file = ".env"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            return cls.json_loads(raw_val)


settings = Settings()


def init_env():
    load_dotenv(dotenv_path=".env")


def get_settings() -> Settings:
    return settings


def is_testing():
    return settings.APP_ENV == "testing"
