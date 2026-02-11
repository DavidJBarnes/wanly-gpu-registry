from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    heartbeat_offline_seconds: int = 120

    model_config = {"env_file": ".env"}


settings = Settings()
