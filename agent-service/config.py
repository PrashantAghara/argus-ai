import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    pprometheus_url: str
    grafana_url: str
    grafana_api_key: str
    postgres_host: str
    postgres_port: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    groq_api_key: str


def get_configs() -> Config:
    return Config(
        pprometheus_url=os.getenv("PROMETHEUS_URL"),
        grafana_url=os.getenv("GRAFANA_URL"),
        grafana_api_key=os.getenv("GRAFANA_API_KEY"),
        postgres_host=os.getenv("POSTGRES_HOST"),
        postgres_port=os.getenv("POSTGRES_PORT"),
        postgres_db=os.getenv("POSTGRES_DB"),
        postgres_user=os.getenv("POSTGRES_USER"),
        postgres_password=os.getenv("POSTGRES_PASSWORD"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )
