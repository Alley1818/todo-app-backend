from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    redis_url: str
    cache_ttl: int
    cache_tasks_key: str
    allowed_origins: list[str] 

def get_settings():
    return Settings(
        DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:15432/postgres",
        redis_url = "redis://localhost:6379/0",
        cache_ttl = 3600,
        cache_tasks_key = "cache:tasks_list",
        allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
    )


