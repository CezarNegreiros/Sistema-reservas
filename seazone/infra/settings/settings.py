from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    SECRET: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )


settings = Settings()
