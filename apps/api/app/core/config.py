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
    EMAIL_NOTIFICATIONS_ENABLED: bool = False
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    ANALYTICS_CACHE_TTL_SECONDS: int = 60
    REDIS_URL: str = "redis://localhost:6379/0"
    JOBS_MAX_RETRIES: int = 3
    ANALYTICS_REFRESH_CRON: str = "*/10 * * * *"
    NOTIFICATIONS_CLEANUP_CRON: str = "0 2 * * *"
    THUMBNAIL_MAX_SIZE: int = 512
    THUMBNAIL_QUALITY: int = 80
    NOTIFICATIONS_RETENTION_DAYS: int = 30
    PUBLIC_API_ENABLED: bool = True
    API_RATE_LIMIT_PER_MINUTE: int = 60
    WEBHOOK_MAX_RETRIES: int = 5
    WEBHOOK_TIMEOUT_SECONDS: int = 5
    WEBHOOK_TOLERANCE_SECONDS: int = 300

    class Config:
        env_file = ".env"


settings = Settings()
