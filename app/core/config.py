from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5432/fastapi_project"
    # здесь мы храним все переменные, которые мы будем хранить для настройки нашего сервиса.
    class Confing:
        env_file = '.env'


settings = Settings()
