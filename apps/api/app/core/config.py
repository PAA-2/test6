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
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: str = (
        "application/pdf,image/png,image/jpeg,"
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document,"
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    UPLOAD_DIR: str = "storage/uploads"

    class Config:
        env_file = ".env"


settings = Settings()
