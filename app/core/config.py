from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    allowed_origins: list[str] 

def get_settings():
    return Settings(
        DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:15432/postgres",
        allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
    )


