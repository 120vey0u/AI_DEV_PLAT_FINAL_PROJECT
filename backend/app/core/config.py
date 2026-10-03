from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    HF_API_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()