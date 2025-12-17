import os

class Settings:
    PROJECT_NAME = "Magazine App"
    VERSION = "1.0.0"
    API_V1_STR = "/api/v1"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mag_user:mag_pass@localhost:5432/mag_db")
    
    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Paths
    OUTPUTS_DIR = os.getenv("OUTPUTS_DIR", "/app/outputs")
    SOURCES_FILE = os.getenv("SOURCES_FILE", os.path.join(OUTPUTS_DIR, "sources.json"))
    CONVOCATORIAS_FILE = os.getenv("CONVOCATORIAS_FILE", os.path.join(OUTPUTS_DIR, "convocatorias.json"))
    
    # Security / Workers
    WORKER_TOKEN = os.getenv("WORKER_TOKEN", "change-me-strong")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    API_INTERNAL_URL = os.getenv("API_INTERNAL_URL", "http://localhost:8000")
    
    # Email
    EMAIL_SETTINGS_FILE = os.getenv("EMAIL_SETTINGS_FILE", "email_settings.json")
    DEFAULT_SENDER_EMAIL = os.getenv("DEFAULT_SENDER_EMAIL", "noreply@cotecmar.com")

settings = Settings()
