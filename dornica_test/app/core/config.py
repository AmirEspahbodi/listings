from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    DB_EMAIL_UNIQUE: bool
    AUTH_ROUTE_PREFIX: str
    
    class Config:
        env_file = '../.env'


settings = Settings()
