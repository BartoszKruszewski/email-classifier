from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    server_email: str = "router-system@example.com"
    ollama_host: str = "http://ollama:11434"
    model_name: str = "qwen2.5:1.5b"
    mailhog_host: str = "mailhog"
    mailhog_port: int = 1025

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
