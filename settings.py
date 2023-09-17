from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SSH_PORT: int = 10022
    HTTP_PORT: int = 10080
    STATUS_INTERVAL: float = 10.0  # Seconds

    model_config = SettingsConfigDict(env_file=".env")


conf = Settings()
