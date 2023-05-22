from pydantic import BaseSettings
from typing import Any


class DBSettings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str


class JWTSettings(BaseSettings):
    # ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: Any
    JWT_ALGORITHM: str
    # CLIENT_ORIGIN: str


class Config:
    env_file = "./.env"


dbsettings = DBSettings()
jwtsettings = JWTSettings()
