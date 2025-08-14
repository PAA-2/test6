from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOW_OWNER_DELETE: bool = True
    PROJECTS_PAGE_SIZE_DEFAULT: int = 10
    PROJECTS_PAGE_SIZE_MAX: int = 100

    class Config:
        env_file = ".env"


settings = Settings()
