from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment.

    API_KEY: Optional shared secret used for simple header-based auth.
    If API_KEY is not set, auth is effectively disabled (for local dev).
    """

    api_key: str | None = None

    class Config:
        env_prefix = ""
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
