from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5433/notes_db"

    class Confing:
        env_file = '.env'


settings = Settings()
