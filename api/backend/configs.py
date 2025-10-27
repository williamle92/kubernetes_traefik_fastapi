import functools
from typing import Optional

from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class Settings(BaseSettings):
    PG_HOST: Optional[str] = Field("db", env="PG_HOST")
    PG_USER: Optional[str] = Field("postgres", env="PG_USER")
    PG_PASSWORD: Optional[str] = Field("password", env="PG_PASSWORD")
    PG_DB: Optional[str] = Field("hyperion", env="PG_DB")
    PG_PORT: Optional[int] = Field(5432, env="PG_PORT")
    PG_URI: Optional[URL] = Field(None)
    SECRET_KEY: Optional[str] = Field("1234", env="SECRET_KEY")
    SALT: Optional[str] = Field("I SEE DEAD PEOPLE", env="SALT")
    ALGORITHM: Optional[str] = Field("HS256")
    REDIS_HOST: Optional[str] = Field("redis", env="REDIS_HOST")

    @field_validator("PG_URI", mode="after")
    def create_db_url(cls, value: Optional[URL], values: ValidationInfo):
        # URL hashes the password
        value: URL = URL.create(
            "postgresql+asyncpg",
            values.data.get("PG_USER"),
            values.data.get("PG_PASSWORD"),
            values.data.get("PG_HOST"),
            values.data.get("PG_PORT"),
        )
        return value


@functools.lru_cache
def get_settings():
    return Settings()


Configs: Settings = get_settings()
